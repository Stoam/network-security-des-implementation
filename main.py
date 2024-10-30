import des

def encrypt():
    # Get DES key from user
    key = des.get_valid_key_input("Enter a 64-bit DES key (in ASCII, 8 characters): ")
    bin_key = des.text_to_binary(key)[0]
    print("DES Key (Hex):", des.binary_to_hex(bin_key))

    # Get user input for plaintext
    plaintext = des.get_valid_text_input("Enter a plaintext (in ASCII, 8 characters): ")

    # Generate round keys
    round_keys = des.generateKeys(bin_key)

    # Encrypt the plaintext
    print("Encrypting...")
    ciphertext = des.encrypt_message(plaintext, round_keys)

    print("Ciphertext (Binary):", ciphertext)
    print("Ciphertext (Hex):", des.binary_to_hex(ciphertext))
    return ciphertext, round_keys

def decrypt(ciphertext, round_keys):
    # Decrypt the encrypted text
    print("Decrypting...")
    plaintext = des.decrypt_message(ciphertext, round_keys)

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
            ciphertext, round_keys = encrypt()
        elif choice == "2":
            if 'ciphertext' not in locals() or 'round_keys' not in locals():
                print("No ciphertext available. Please perform encryption first.")
            else:
                decrypt(ciphertext, round_keys)
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")
