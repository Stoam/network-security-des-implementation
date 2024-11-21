import socket
import des
import rsa

def register_with_pka(public_key):
    pka_host = socket.gethostname()
    pka_port = 6000  # Port of the PKA

    pka_socket = socket.socket()
    pka_socket.connect((pka_host, pka_port))

    # Register the server's public key
    server_name = "Server1"  # Example server name
    request = f"REGISTER:{server_name}:{public_key}"
    pka_socket.send(request.encode())
    response = pka_socket.recv(1024).decode()
    print("Response from PKA:", response)

    pka_socket.close()

def server_program():
    # Generate RSA key pair
    public_key, private_key = rsa.generate_rsa_keys()
    print("RSA Public Key:", public_key)

    # Register with the PKA
    register_with_pka(public_key)

    # Host and port setup
    host = socket.gethostname()
    port = 5000
    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(2)
    print(f"Server started on {host}:{port}. Waiting for a connection...")

    conn, address = server_socket.accept()
    print("Connection from:", str(address))

    # Receive the encrypted DES key
    encrypted_des_key = eval(conn.recv(1024).decode())
    des_key = rsa.rsa_decrypt(private_key, encrypted_des_key)
    print("DES Key received and decrypted:", des_key)

    bin_key = des.text_to_binary(des_key)[0]
    print("DES Key (Hex):", des.binary_to_hex(bin_key))

    # Send acknowledgment
    conn.send("DES Key received successfully.".encode())

    # Decrypt the incoming message
    round_keys = des.generateKeys(bin_key)
    ciphertext = conn.recv(1024).decode()
    plaintext = des.decrypt_message(ciphertext, round_keys)
    print("Decrypted message:", plaintext)

    conn.close()

if __name__ == "__main__":
    server_program()
