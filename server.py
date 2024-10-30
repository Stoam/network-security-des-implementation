import socket
import des

def get_valid_ascii_input(prompt):
    while True:
        ascii_input = input(prompt)
        if len(ascii_input) == 8:
            return ascii_input
        else:
            print("Input must be 8 characters long.")

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
    key = get_valid_ascii_input("Enter a 64-bit DES key (in ASCII, 8 characters): ")
    bin_key = des.text_to_binary(key)[0]
    print("DES Key (Hex):", des.binary_to_hex(bin_key))

    print("Waiting for encrypted message from the client...")

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
