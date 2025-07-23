import socket
import featuresChat

HOST = input("Enter the server's IP Address: ")
PORT = int(input("Enter the port server is using for this chat: "))
try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST,PORT))
        transferingFile = False
        while True:
            if transferingFile:
                featuresChat.receive_file(file,sock,size)
                transferingFile = False
            msg = ""
            while (msg == ""):
                msg = input("Enter the message you want to send to Server (can't be empty): ")
            if msg == "/sendfile":
                file = featuresChat.send_file_data(sock)
            else:
                sock.sendall(msg.encode("utf-8", errors="ignore"))
            data = sock.recv(1024)
            data = data.decode("utf-8", errors="ignore")
            if msg == "/sendfile":
                featuresChat.manage_send_file_response(file, sock, data)
            if data == "/sendfile":
                msg, file, size, transferingFile = featuresChat.manage_send_file_req(sock)
            elif not data or data.lower() == "exit":
                break
            else:
                print(f'Server said: {data}')
        if msg.lower() != "exit":
            print("Server closed the chat :(")
except Exception as e:
    print(f"An exception raised: {e}")
finally:
    print("Closing connection...")