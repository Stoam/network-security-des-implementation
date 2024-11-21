import socket

# Simulated public key database (server_name -> public_key)
PUBLIC_KEY_DB = {}

def pka_program():
    host = socket.gethostname()
    port = 6000  # PKA runs on a different port

    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(5)
    print("Public Key Authority (PKA) started...")

    while True:
        conn, address = server_socket.accept()
        print("Connection from:", str(address))

        # Receive request: either "REGISTER:<key>" or "REQUEST:<server_name>"
        request = conn.recv(1024).decode()
        if request.startswith("REGISTER:"):
            # Register the public key
            _, server_name, public_key = request.split(":", 2)
            PUBLIC_KEY_DB[server_name] = eval(public_key)  # Store as tuple
            response = f"Public key for {server_name} registered successfully."
            conn.send(response.encode())
        elif request.startswith("REQUEST:"):
            # Provide the public key
            _, server_name = request.split(":")
            public_key = PUBLIC_KEY_DB.get(server_name)
            if public_key:
                conn.send(str(public_key).encode())
            else:
                conn.send("Error: Public key not found.".encode())
        else:
            conn.send("Invalid request.".encode())

        conn.close()

if __name__ == "__main__":
    pka_program()
