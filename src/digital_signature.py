import binascii
import hashlib
import ecdsa

def sign_message(message, private_key):
    # The message needs to be bytes, so we'll convert
    message = message.encode('utf8')

    # Hash the message
    hashed_message = hashlib.sha256(message).digest()

    # Generate the signature
    signature = private_key.sign(hashed_message)
    
    return signature

def verify_signature(message, signature, public_key):
    # The message needs to be bytes, so we'll convert
    message = message.encode('utf8')

    # Hash the message
    hashed_message = hashlib.sha256(message).digest()

    try:
        # Verify the signature
        public_key.verify(signature, hashed_message)
        return True
    except ecdsa.BadSignatureError:
        return False
    
def show_curve_options():
    print("Available curve options for generating private keys:")
    print("1. NIST256p")
    print("2. NIST384p")
    print("3. NIST521p")
    print("4. BRAINPOOLP256r1")
    print("5. BRAINPOOLP384r1")
    print("6. BRAINPOOLP512r1")
    print("7. SECP128r1")
    print("8. SECP160r1")
    print("9. SECP256k1")
    print("10. Ed25519")

def generate_key_pair(curve_option):
    if curve_option == 1:
        curve = ecdsa.NIST256p
    elif curve_option == 2:
        curve = ecdsa.NIST384p
    elif curve_option == 3:
        curve = ecdsa.NIST521p
    elif curve_option == 4:
        curve = ecdsa.BRAINPOOLP256r1
    elif curve_option == 5:
        curve = ecdsa.BRAINPOOLP384r1
    elif curve_option == 6:
        curve = ecdsa.BRAINPOOLP512r1
    elif curve_option == 7:
        curve = ecdsa.SECP128r1
    elif curve_option == 8:
        curve = ecdsa.SECP160r1
    elif curve_option == 9:
        curve = ecdsa.SECP256k1
    elif curve_option == 10:
        curve = ecdsa.Ed25519
    else:
        raise ValueError("Invalid curve option")

    private_key = ecdsa.SigningKey.generate(curve=curve)
    public_key = private_key.get_verifying_key()

    return private_key, public_key

def save_key_pair(private_key, public_key):
    with open("key/private.pem", "wb") as f:
        f.write(private_key.to_pem())
    with open("key/public.pem", "wb") as f:
        f.write(public_key.to_pem())

def save_message_with_signature(name, title, date, private_key):
    message = "Name: {}\nTitle: {}\nDate: {}\n".format(name, title, date)

    # Sign the message
    signature = sign_message(message, private_key)

    # Save the message and signature to a file
    with open("message_with_signature.txt", "w") as file:
        file.write(message)
        file.write("Digital Signature: {}".format(binascii.hexlify(signature).decode()))
        file.write("\n-----END OF MESSAGE-----")

def verify_signature_with_public_key(message, public_key):
    # Read the message file
    with open(message, "r") as file:
        message_content = file.read().strip()

    # Extract the signature from the message
    signature_start_index = message_content.rfind("Digital Signature: ") + len("Digital Signature: ")
    signature_str = message_content[signature_start_index:]

    # Remove the signature from the message content
    message_content = message_content[:signature_start_index-len("Digital Signature: ")]


    # Convert the signature from hex string to bytes
    try:
        signature = binascii.unhexlify(signature_str)
    except:
        raise ValueError("There is no signature in image or argument not contain ASCII characters")
    # print("signature verify:\n" + binascii.hexlify(signature).decode())

    # Verify the signature
    is_verified = verify_signature(message=message_content, signature=signature , public_key=public_key)
    

    return is_verified

def main_generate_digital_signature():
    # Show available curve options
    name = input("Enter the artist's name: ")
    title = input("Enter the painting's title: ")
    date = input("Enter the painting's creation date: ")
    show_curve_options()

    # User input
    curve_option = int(input("Enter the curve option for generating private keys: "))

    # Generate key pair
    private_key, public_key = generate_key_pair(curve_option)

    # Save key pair to file
    save_key_pair(private_key, public_key)

    # Save message with signature to file
    save_message_with_signature(name, title, date, private_key)

    print("Digital signature and key pair files created successfully.")

def main_verify_digital_signature(pubkey_file, message_file):
    # Read the public key file from user input
    public_key = ecdsa.VerifyingKey.from_pem(open(pubkey_file).read())

    # Verify the digital signature
    try:
        is_verified = verify_signature_with_public_key(message_file, public_key)
    except ecdsa.MalformedPointError:
        print("Error: Invalid public key format.")
        return

    if is_verified:
        print("Digital signature is verified.")
    else:
        print("Digital signature is NOT verified.")
