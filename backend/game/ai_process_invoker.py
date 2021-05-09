from model.decision import Decision
from game.ai_bridge import AiBridge
from queue import Queue, Empty
from threading import Thread
import subprocess
import sys
import time
import os


class AiProcessInvoker:
    def __init__(self):
        pass

    def start_process(self):
        DETACH = 0x8
        self._process = subprocess.Popen(['py', '-3', 'ai_process.py'], shell=False,
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=None, creationflags=DETACH)
        self._queue = Queue()
        self._queue_stderr = Queue()
        self._thread = Thread(target=self.enqueue_output)
        self._thread.start()
        self._thread_stderr = Thread(target=self.enqueue_stderr)
        self._thread_stderr.start()

    def enqueue_output(self):
        for line in iter(self._process.stdout.readline, b''):
            self._queue.put(line)

    def enqueue_stderr(self):
        for line in iter(self._process.stderr.readline, b''):
            self._queue_stderr.put(line)

    def get_decision(self, symbols_json):
        self._process.stdin.write(symbols_json.encode() + b'\r\n')
        self._process.stdin.flush()
        while True:
            try:
                comm = self._queue.get_nowait()
            except Empty:
                time.sleep(0.1)
            else:
                break
        try:
            err = self._queue_stderr.get_nowait()
        except Empty:
            pass
        else:
            print(err)
        self._process.stdout.flush()
        self._process.stderr.flush()
        comm = comm[:-2]
        print(comm)
        return Decision.from_json(comm.decode()) 

    def load_dll(self):
        self._ai_bridge = AiBridge()

    def get_decision_from_dll(self):
        json_symbols = input()
        print(self._ai_bridge.get_decision(json_symbols).to_json())
