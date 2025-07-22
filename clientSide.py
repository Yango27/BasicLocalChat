import socket
import featuresChat

HOST = input("Enter the server's IP Address: ")
PORT = int(input("Enter the port server is using for this chat: "))

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST,PORT))

while True:
    msg = ""
    while (msg == ""):
        msg = input("Enter the message you want to send to Server (can't be empty): ")
    if msg == "/sendfile":
        file = featuresChat.send_file_data(sock)
    else:
        sock.sendall(msg.encode("utf-8", errors="ignore"))
    data = sock.recv(1024)
    if not data or data.decode("utf-8", errors="ignore").lower() == "exit":
        break
    elif data.decode("utf-8", errors="ignore") == "Accepted" and msg == "/sendfile":
        print("The other side accepted the file transfer :)")
        featuresChat.send_file(file, sock)
    elif data.decode("utf-8", errors="ignore") == "Rejected" and msg == "/sendfile":
        print("The other side rejected the file transfer :(")
        file.close()
    else:
        print(f'Server said: {data.decode("utf-8", errors = "ignore")}')

if msg.lower() != "exit":
    print("Server closed the chat :(")
print("Closing connection...")
sock.close()