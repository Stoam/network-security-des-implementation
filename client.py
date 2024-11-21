import socket
import des
import rsa

def request_public_key(server_name):
    pka_host = socket.gethostname()
    pka_port = 6000  # Port of the PKA

    pka_socket = socket.socket()
    pka_socket.connect((pka_host, pka_port))

    # Request the server's public key
    request = f"REQUEST:{server_name}"
    pka_socket.send(request.encode())
    response = pka_socket.recv(1024).decode()

    pka_socket.close()
    if "Error" in response:
        print(response)
        return None
    return eval(response)  # Convert string to tuple

def client_program():
    host = socket.gethostname()
    port = 5000

    client_socket = socket.socket()
    client_socket.connect((host, port))

    # Request server's public key from the PKA
    server_name = "Server1"
    public_key = request_public_key(server_name)
    if not public_key:
        print("Failed to obtain server's public key.")
        client_socket.close()
        return

    print("Received RSA Public Key:", public_key)

    # Encrypt the DES key
    des_key = des.get_valid_key_input("Enter a 64-bit DES key (in ASCII, 8 characters): ")
    encrypted_des_key = rsa.rsa_encrypt(public_key, des_key)
    client_socket.send(str(encrypted_des_key).encode())
    print("Encrypted DES key sent to the server.")

    # Encrypt and send message
    plaintext = des.get_valid_text_input("Enter a plaintext (in ASCII): ")
    round_keys = des.generateKeys(des.text_to_binary(des_key)[0])
    ciphertext = des.encrypt_message(plaintext, round_keys)
    client_socket.send(ciphertext.encode())
    print("Encrypted message sent.")

    client_socket.close()

if __name__ == "__main__":
    client_program()
