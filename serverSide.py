import socket
import featuresChat
HOST = "0.0.0.0"
PORT = int(input("Enter the port you want to use for this Chat: "))
try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((HOST,PORT))
        sock.listen()
        print(f"Listening on {HOST} : {PORT}")
        conn, addr = sock.accept()
        with conn:
            print(f"Client connected from {addr[0]} : {addr[1]}")
            transferingFile = False
            msg = ""
            while True:
                if transferingFile:
                    featuresChat.receive_file(file,conn,size)
                    transferingFile = False
                else:
                    data = conn.recv(1024)
                    data = data.decode('utf-8', errors="ignore")
                    if msg == "/sendfile":
                        featuresChat.manage_send_file_response(file, conn, data)
                    if not data or data.lower() == "exit":
                        break
                    elif data == "/sendfile":
                        msg, file, size, transferingFile = featuresChat.manage_send_file_req(conn)
                    else:
                        print(f'Client said: {data}')
                        msg = ""
                        while (msg == ""):
                            msg = input("Enter the message you want to sent to Client (can't be empty): ")
                        if msg == "/sendfile":
                            file = featuresChat.send_file_data(conn)
                    if msg != "/sendfile":
                        conn.sendall(msg.encode("utf-8", errors="ignore"))
            if msg.lower() != "exit":
                print("Client closed the chat :(")
except Exception as e:
    print(f"An exception raised: {e}")
finally:
    print("Closing the connection...")
