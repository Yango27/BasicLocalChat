import socket

def send_file_data(s : socket.socket):
    while True:
        filePath = input("Enter the path of the file you want to send: ")
        try:
            f = open(filePath, "rb") #reads the file's bytes
            break
        except Exception as e:
            print(f"An exception raised: {e}. Try again!")
    s.sendall("/sendfile".encode("utf-8", errors="ignore")) #first we send the command so the other side knows we want to send a file
    f.seek(0,2) #goes to the end of the file 
    size = f.tell() 
    msg = f'File Name : {f.name}, Size (bytes): {size}'
    s.recv(1024) #waits the other side for sending the file's data
    s.sendall(msg.encode("utf-8", errors="ignore")) #sends the file information to the other side
    f.seek(0)
    return f

def send_file(file , s : socket.socket):
    chunk = file.read(4096) 
    while chunk != b"": #while is not completely sent
        s.sendall(chunk) #sending the file's bytes chunk by chunk
        chunk = file.read(4096)
    print("File sent!")
    file.close()

def manage_send_file_response(file, s : socket.socket, data : str):
    if data == "Accepted":
        print("The other side accepted the file transfer :)")
        send_file(file, s)
    else:
        print("The other side rejected the file transfer :(")
        file.close()

def manage_send_file_req(s):
    s.sendall("Go on".encode("utf-8", errors="ignore")) #tells the other side to send the file's data
    data = s.recv(1024) #here we want to wait for the file data
    data = data.decode("utf-8", errors="ignore")
    print("You received a file transfer request!")
    print(data)
    response = ""
    size = 0
    f = None
    while response.lower() != "yes" and response.lower() != "no":
        response = input("Do you want to accept this file transfer?: (yes/no)")
        if (response.lower() == "yes"):
            print("You accepted the file transfer :)")
            msg = "Accepted"
            while True: #ensuring there are no errors
                filePath = input("Enter the path where you want to save your file (Remember to include file name and extension): ")
                try:
                    f = open(filePath, "wb")
                    break
                except Exception as e:
                    print(f"An exception raised: {e}. Try again!")
            size = int(data.split(",")[1].split(":")[1].strip())
            transferingFile = True
        elif (response.lower() == "no"):
            print("You rejected the file transfer :(")
            msg = "Rejected"
            transferingFile = False
    return msg, f, size, transferingFile

def receive_file(f, s : socket.socket , size : int):
    try:
        bytesRead = 0
        while bytesRead < size:
            chunk = s.recv(min(4096, size-bytesRead)) #normally a chunk size would be 4096, the only exception could be last one
            f.write(chunk)
            bytesRead += len(chunk)
        print("File received!")
    finally:
        f.close()

