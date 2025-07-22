import socket
import featuresChat
HOST = "0.0.0.0"
PORT = int(input("Enter the port you want to use for this Chat: "))

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
sock.bind((HOST,PORT))
sock.listen()
print(f"Listening on {HOST} : {PORT}")
conn, addr = sock.accept()
print(f"Client connected from {addr[0]} : {addr[1]}")
transferingFile = False
while True:
    msg = ""
    if transferingFile:
        featuresChat.receive_file(file,conn,size)
        transferingFile = False
    else:
        data = conn.recv(1024)
    if not data or data.decode('utf-8', errors="ignore").lower() == "exit":
        break
    elif data.decode('utf-8', errors="ignore").lower() == "/sendfile":
        msg, file, size, transferingFile = featuresChat.manage_send_file_req(conn)
    else:
        print(f'Client said: {data.decode("utf-8", errors="ignore")}')
        while (msg == ""):
            msg = input("Enter the message you want to sent to Client (can't be empty): ")
    conn.sendall(msg.encode("utf-8", errors="ignore"))
    
if msg.lower() != "exit":
    print("Client closed the chat :(")

print("Closing the connection...")
conn.close()
sock.close()
