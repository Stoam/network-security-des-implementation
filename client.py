import socket
import des

def get_valid_ascii_input(prompt):
    while True:
        ascii_input = input(prompt)
        if len(ascii_input) > 0:
            
            return ascii_input
        else:
            print("Input cannot be empty.")

def client_program():
    host = socket.gethostname()
    port = 5000

    client_socket = socket.socket()
    client_socket.connect((host, port))  # Connect to the server

    # Get user input for plaintext
    plaintext = get_valid_ascii_input("Enter a plaintext (in ASCII): ")

    # Get DES key from user
    key = get_valid_ascii_input("Enter a 64-bit DES key (in ASCII, 8 characters): ")
    bin_key = des.text_to_binary(key)[0]
    print("DES Key (Hex):", des.binary_to_hex(bin_key))

    # Generate round keys
    round_keys = des.generateKeys(bin_key)

    # Encrypt the plaintext
    ciphertext = des.encrypt_message(plaintext, round_keys)

    # Send encrypted message to the server
    print("Sending encrypted message...")
    client_socket.send(ciphertext.encode())  # Send ciphertext

    # Close the connection
    client_socket.close()
    print("Message sent. Connection closed.")

if __name__ == '__main__':
    client_program()