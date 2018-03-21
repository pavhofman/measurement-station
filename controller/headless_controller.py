import netifaces as ni
import os
import socket
import threading
from queue import Queue, Empty
from typing import Iterator, Tuple

import dbus
import pyttsx3
import time

import config

# maximum delay between two powerbutton presses to run shutdown
PBTN_TIMEOUT = 2

def iterIfaceIP() -> Iterator[Tuple[str, str]]:
    for iface in ni.interfaces():
        if iface == 'lo':
            continue
        if ni.AF_INET in ni.ifaddresses(iface) \
                and len(ni.ifaddresses(iface)[ni.AF_INET]) > 0 \
                and 'addr' in ni.ifaddresses(iface)[ni.AF_INET][0]:
            ip = ni.ifaddresses(iface)[ni.AF_INET][0]['addr']
            yield iface, ip


class VoiceAssistant(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self._engine = pyttsx3.init()
        self._engine.setProperty('rate', 100)
        self._engine.setProperty('voice', 'english')
        self._umuteSoundcard()

        self._q = Queue()
        self.daemon = True

    def _umuteSoundcard(self):
        os.system('/usr/bin/amixer -c %s set Master 100 unmute' % config.PC_SPEAKER_NAME)

    def addSay(self, msg):
        print(msg)
        self._q.put(msg)

    def run(self):
        while True:
            self._engine.say(self._q.get())
            self._engine.runAndWait()
            self._q.task_done()

    def stopTalking(self):
        self._clearQueue()
        self._engine.stop()

    def _clearQueue(self):
        while not self._q.empty():
            try:
                self._q.get(False)
            except Empty:
                continue
            self._q.task_done()


class PowerBtnMonitor:
    def __init__(self, talker: VoiceAssistant) -> None:
        self._talker = talker
        self._s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self._s.connect("/var/run/acpid.socket")
        print("Connected to acpid")
        self._count = 0
        self._sayIPs()

    def _timerExpired(self):
        self._count = 0

    def _pbtnPressed(self) -> None:
        print('power_button: %d' % self._count)
        self._talker.stopTalking()
        if self._count <= 1:
            # first press
            timer = threading.Timer(PBTN_TIMEOUT, self._timerExpired)
            timer.start()
            self._sayIPs()
        else:
            # managed to press within interval, shutting down
            self._talker.addSay('Shutting down. Have a nice day.')
            # allow enought time for talk
            time.sleep(6)
            if (config.DO_POWER_OFF):
                self._powerOff()

    def _powerOff(self):
        sys_bus = dbus.SystemBus()
        lg = sys_bus.get_object('org.freedesktop.login1', '/org/freedesktop/login1')
        pwr_mgmt = dbus.Interface(lg, 'org.freedesktop.login1.Manager')
        shutdown_method = pwr_mgmt.get_dbus_method("PowerOff")
        shutdown_method(True)

    def run(self):
        while 1:
            recv = self._s.recv(4096).decode()
            for event in recv.split('\n'):
                event = event.split(' ')
                if len(event) < 2: continue
                #print(str(event))
                if config.check_acpi_event(event):
                    # Power button pressed
                    self._count += 1
                    self._pbtnPressed()

    def _sayIPs(self):
        ipsByName = dict((iface, ip) for iface, ip in iterIfaceIP())
        if len(ipsByName) == 0:
            self._talker.addSay('No network connection found')
        else:
            self._talker.addSay('Network addresses')
            for iface in ipsByName.keys():
                sayIP = False
                if iface.startswith('wl'):
                    self._talker.addSay('wifi')
                    sayIP = True
                elif iface.startswith('en'):
                    self._talker.addSay('cable')
                    sayIP = True
                if sayIP:
                    self._talker.addSay(ipsByName[iface])


if __name__ == "__main__":
    talker = VoiceAssistant()
    talker.start()
    monitor = PowerBtnMonitor(talker)
    monitor.run()
