#!/usr/bin/env python3
import asyncio
import signal
import os
import logging
import sys

_name = 0
log = logging.getLogger("gsrun")

NEVER = 0
ON_FAILURE = 1
ALLWAYS = 2
KILL_PARENT = 3


class Process:
    def __init__(
        self,
        prog,
        *params,
        stop_signal=signal.SIGTERM,
        uid=None,
        gid=None,
        groups=None,
        restart_policy=NEVER,
        name=None,
    ):
        global _name
        self.cmd = (prog,) + params
        self.stop_signal = stop_signal
        self.proc = None
        self.uid = uid
        self.gid = gid
        self.groups = groups
        self.restart_policy = restart_policy
        self.signal_sent = False
        if name is None:
            self.name = f"Process {_name}"
            _name += 1

    async def start(self):
        self.proc = await asyncio.create_subprocess_exec(
            *self.cmd, start_new_session=True, preexec_fn=self.preexec_fn
        )
        log.info(f"STARTED: {self}")

    def preexec_fn(self):
        if self.gid:
            os.setgid(self.gid)
        if self.uid:
            os.setuid(self.uid)
        if self.groups:
            os.setgroups(self.groups)

    def __str__(self):
        retcode = "-" if not self.proc else self.proc.returncode
        return f"{self.name}: (returncode {retcode})"


class ProcessList:
    def __init__(self, *processes):
        self.processes = processes
        self.terminated = False
        self.signal_received = False
        self.main_exit = 0

    def stop_processes(self):
        self.terminated = True
        for p in self.processes:
            if p.proc and p.proc.returncode is None and not p.signal_sent:
                log.debug(f"STOPPING {p} - sending signal#{p.stop_signal}")
                p.proc.send_signal(p.stop_signal)
                p.signal_sent = True

    async def start(self):
        original_sigterm_handler = signal.getsignal(signal.SIGTERM)
        original_sigint_handler = signal.getsignal(signal.SIGINT)

        def handler(signum, frame):
            self.signal_received = True

        signal.signal(signal.SIGTERM, handler)
        signal.signal(signal.SIGINT, handler)

        for p in self.processes:
            if self.signal_received:
                break
            await p.start()

        if self.signal_received:
            self.stop_processes()

        # waiting for process completion
        others = {p for p in self.processes if p.proc}
        while others:
            wait_set = set()
            for p in others:
                if p.proc:
                    t = asyncio.create_task(p.proc.wait())
                    t._process = p
                    wait_set.add(t)
            completed, others = await asyncio.wait(
                wait_set, return_when=asyncio.FIRST_COMPLETED, timeout=1
            )
            completed = {c._process for c in completed}
            others = {o._process for o in others}
            if self.signal_received:
                self.stop_processes()
            if completed:
                for comp in completed:
                    retcode = comp.proc.returncode
                    if self.terminated:
                        log.info(f"EXITED: {comp}")
                    else:
                        if retcode == 0:
                            log.info(f"EXITED normally: {comp}")
                        else:
                            log.warning(f"EXITED with failure: {comp}")
                            if comp.restart_policy == ON_FAILURE:
                                log.info(
                                    f"RESTARTING {comp} (restart_policy = ON_FAILURE)"
                                )
                                await comp.start()
                                others.add(comp)
                        if comp.restart_policy == ALLWAYS:
                            log.info(f"RESTARTING {comp} (restart_policy = ALLWAYS)")
                            await comp.start()
                            others.add(comp)
                        if comp.restart_policy == KILL_PARENT:
                            self.main_exit = comp.proc.returncode
                            self.stop_processes()

        # cleanup
        signal.signal(signal.SIGTERM, original_sigterm_handler)
        signal.signal(signal.SIGINT, original_sigint_handler)
        log.debug(f"RETURNCODE: {self.main_exit}")
        return self.main_exit


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    ret = asyncio.run(
        ProcessList(
            Process("ls", "-al"),
            # Process("id", uid=6),
            Process("./bad.py", stop_signal=signal.SIGINT, restart_policy=KILL_PARENT),
            Process("./good.py", stop_signal=signal.SIGINT, restart_policy=KILL_PARENT),
        ).start()
    )
    sys.exit(ret)
