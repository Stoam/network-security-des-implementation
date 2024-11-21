import random

# Helper function to compute gcd
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

# Helper function to compute modular inverse
def mod_inverse(e, phi):
    d, x1, x2, y1 = 0, 0, 1, 1
    temp_phi = phi

    while e > 0:
        temp1 = temp_phi // e
        temp2 = temp_phi - temp1 * e
        temp_phi, e = e, temp2

        x = x2 - temp1 * x1
        y = d - temp1 * y1

        x2, x1 = x1, x
        d, y1 = y1, y

    if temp_phi == 1:
        return d + phi

# Generate a random prime number
def generate_prime(start, end):
    while True:
        num = random.randint(start, end)
        if is_prime(num):
            return num

# Check if a number is prime
def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

# RSA key generation
def generate_rsa_keys():
    # Generate two large primes
    p = generate_prime(100, 200)  # Example range; increase for better security
    q = generate_prime(100, 200)

    n = p * q
    phi = (p - 1) * (q - 1)

    # Choose e
    e = random.randint(2, phi - 1)
    while gcd(e, phi) != 1:
        e = random.randint(2, phi - 1)

    # Compute d
    d = mod_inverse(e, phi)

    # Public key (e, n), Private key (d, n)
    return (e, n), (d, n)

# RSA encryption
def rsa_encrypt(public_key, plaintext):
    e, n = public_key
    ciphertext = [pow(ord(char), e, n) for char in plaintext]
    return ciphertext

# RSA decryption
def rsa_decrypt(private_key, ciphertext):
    d, n = private_key
    plaintext = ''.join([chr(pow(char, d, n)) for char in ciphertext])
    return plaintext
