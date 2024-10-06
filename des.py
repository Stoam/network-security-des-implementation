import table as t

# Convert text to binary representation
def text_to_binary(text):
    binary_result = ""
    for char in text:
        binary_char = bin(ord(char))[2:].zfill(8)
        binary_result += binary_char

    # Split into 64-bit chunks
    return [binary_result[i:i+64] for i in range(0, len(binary_result), 64)]

# Convert binary to text (ASCII decoding)
def binary_to_text(binary_list):
    binary_str = ''.join(binary_list)
    text = ""
    for i in range(0, len(binary_str), 8):
        char_binary = binary_str[i:i+8]
        char = chr(int(char_binary, 2))
        text += char
    return text

# Convert binary string to hexadecimal representation
def binary_to_hex(binary_str):
    return format(int(binary_str, 2), 'X').zfill(len(binary_str) // 4)

# Permutation function
def permute(source, table):
    return ''.join(source[i - 1] for i in table)

# Perform left shift on a binary string
def left_shift_binary(binary_str, n):
    return binary_str[n:] + binary_str[:n]

# XOR two binary strings
def binary_xor(bin_str1, bin_str2):
    return ''.join('0' if a == b else '1' for a, b in zip(bin_str1.zfill(len(bin_str2)), bin_str2.zfill(len(bin_str1))))

# Convert a decimal number to a 4-bit binary string
def decimal_to_binary(decimal):
    return bin(decimal)[2:].zfill(4)

# Generate 16 round keys from a single 64-bit key
def generateKeys(key):
    round_keys = []
    # 64 bits to 56 bits, remove parity bits
    pc1_key = permute(key, t.pc1)
    left, right = pc1_key[:28], pc1_key[28:]

    for i in range(16):
        # Perform left shifts
        left = left_shift_binary(left, t.shift_round[i])
        right = left_shift_binary(right, t.shift_round[i])

        # Combine left and right, and compress them to 48 bits using pc2
        round_key = permute(left + right, t.pc2)
        round_keys.append(round_key)

    return round_keys

# DES encryption function (single block)
def encrypt(plaintext, round_keys):
    # Initial permutation
    ip_plaintext = permute(plaintext, t.init_perm)
    left, right = ip_plaintext[:32], ip_plaintext[32:]

    for i in range(16):  # 16 rounds
        # Expand right side from 32 to 48 bits
        right_expanded = permute(right, t.exp_perm)

        # XOR with round key
        right_xored = binary_xor(right_expanded, round_keys[i])

        # Apply S-boxes (convert 48 bits back to 32 bits)
        right_sboxed = ""
        for j in range(0, 48, 6):
            chunk = right_xored[j:j+6]
            row = int(chunk[0] + chunk[5], 2)
            col = int(chunk[1:5], 2)
            right_sboxed += decimal_to_binary(t.sbox_perm[j//6][row][col])

        # Permute using P-box
        right_pboxed = permute(right_sboxed, t.pbox_perm)

        # XOR with left side
        right_result = binary_xor(left, right_pboxed)
        left, right = right, right_result

    # Final permutation (combine left and right and inverse initial permutation)
    return permute(right + left, t.inv_init_perm)

# DES decryption function (single block)
def decrypt(ciphertext, round_keys):
    rev_round_keys = round_keys[::-1]
    return encrypt(ciphertext, rev_round_keys)
