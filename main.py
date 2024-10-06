import des

def get_valid_binary_input(prompt, length):
    while True:
        binary_input = input(prompt)
        if all(c in '01' for c in binary_input) and len(binary_input) == length:
            return binary_input
        else:
            print(f"Invalid input. Please provide a {length}-bit binary string.")

def get_valid_ascii_input(prompt, length):
    while True:
        ascii_input = input(prompt)
        if len(ascii_input) == length:
            return ascii_input
        else:
            print(f"Invalid input. Please provide exactly {length} characters.")

def encrypt_message():
    plaintext = get_valid_ascii_input("Enter a plaintext (in ASCII, 8 characters): ", 8)
    bin_plaintext = des.text_to_binary(plaintext)[0]

    key = get_valid_ascii_input("Enter a 64-bit DES key (in ASCII, 8 characters): ", 8)
    bin_key = des.text_to_binary(key)[0]
    print("DES Key (Hex):", des.binary_to_hex(bin_key))

    round_keys = des.generateKeys(bin_key)

    print("Encrypting...")
    ciphertext = des.encrypt(bin_plaintext, round_keys)

    print("Ciphertext (Binary):", ciphertext)
    print("Ciphertext (Hex):", des.binary_to_hex(ciphertext))
    return ciphertext, round_keys

def decrypt_message(ciphertext, round_keys):
    print("Decrypting...")
    plaintext_binary = des.decrypt(ciphertext, round_keys)
    plaintext = des.binary_to_text(plaintext_binary)

    print("Recovered Plaintext:", plaintext)
    return plaintext

if __name__ == "__main__":
    while True:
        print("\nDES Encryption/Decryption")
        print("1. Encrypt")
        print("2. Decrypt")
        print("3. Exit")
        choice = input("Choose an option (1/2/3): ")

        if choice == "1":
            ciphertext, round_keys = encrypt_message()
        elif choice == "2":
            if 'ciphertext' not in locals() or 'round_keys' not in locals():
                print("No ciphertext available. Please perform encryption first.")
            else:
                decrypt_message(ciphertext, round_keys)
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")
