import socket

ip = input("Enter IP address or hostname: ")
port = int(input("Enter port number: "))

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(3)

result = sock.connect_ex((ip, port))

if result == 0:
    print("Status: OPEN")
else:
    print("Status: CLOSED or UNREACHABLE")

sock.close()