import socket
import des

def server_program():
    # Get the hostname
    host = socket.gethostname()
    port = 5000

    server_socket = socket.socket()
    server_socket.bind((host, port))  # Bind host address and port together

    # Server can listen for a connection
    server_socket.listen(2)
    
    print(f"Server started. Waiting for a connection on {host}:{port}...")
    
    conn, address = server_socket.accept()  # Accept a new connection
    print("Connection from:", str(address))

    # Get the decryption key
    key = des.get_valid_key_input("Enter a 64-bit DES key (in ASCII, 8 characters): ")
    bin_key = des.text_to_binary(key)[0]
    print("DES Key (Hex):", des.binary_to_hex(bin_key))

    print("Waiting for the client's key...")

    # Receive the client's key
    client_key = conn.recv(1024).decode()

    # Check if keys match
    if client_key != key:
        error_message = "Error: Keys do not match. Connection will be closed."
        conn.send(error_message.encode())
        print(error_message)
        conn.close()
        return
    
    # Send acknowledgment
    ack = "Key received."
    conn.send(ack.encode())

    print(ack + " Waiting for encrypted message from the client...")

    # Generate round keys
    round_keys = des.generateKeys(bin_key)

    # Receive ciphertext
    ciphertext = conn.recv(1024).decode()  # Receive encrypted message
    print("Encrypted message received.")

    # Decrypt the received message
    plaintext = des.decrypt_message(ciphertext, round_keys)
    print("Decrypted message:", plaintext)

    # Close the connection
    conn.close()
    print("Connection closed.")

if __name__ == '__main__':
    server_program()
