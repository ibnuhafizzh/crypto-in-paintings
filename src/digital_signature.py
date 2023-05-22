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

def generate_key_pair(curve_option):
    if curve_option == 1:
        curve = ecdsa.NIST256p
    elif curve_option == 2:
        curve = ecdsa.NIST384p
    elif curve_option == 3:
        curve = ecdsa.NIST521p
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
    # print("original msg:\n" + message)
    print("signature generate:\n" + binascii.hexlify(signature).decode())

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
    # print(signature_str)

    # Remove the signature from the message content
    message_content = message_content[:signature_start_index-len("Digital Signature: ")]
    # print("read msg from file:\n" + message_content)


    # Convert the signature from hex string to bytes
    try:
        signature = binascii.unhexlify(signature_str)
    except:
        raise ValueError("There is no signature in image or argument not contain ASCII characters")
    # print("signature verify:\n" + binascii.hexlify(signature).decode())


    # Hash the message content

    # Verify the signature
    is_verified = verify_signature(message=message_content, signature=signature , public_key=public_key)
    

    return is_verified

def main_generate_digital_signature():
    # Show available curve options
    show_curve_options()

    # User input
    curve_option = int(input("Enter the curve option for generating private keys: "))
    name = input("Enter your name: ")
    title = input("Enter the title: ")
    date = input("Enter the date: ")

    # Generate key pair
    private_key, public_key = generate_key_pair(curve_option)

    # Save key pair to file
    save_key_pair(private_key, public_key)

    # Save message with signature to file
    save_message_with_signature(name, title, date, private_key)

    print("Digital signature and key pair files created successfully.")

def main_verify_digital_signature(pubkey_file, message_file):
    # Read the public key file from user input
    # pubkey_file = input("Enter the public key file (.pem) : ")
    public_key = ecdsa.VerifyingKey.from_pem(open(pubkey_file).read())

    # Verify the digital signature
    # message_file = input("Enter the message file (.txt) : ")
    try:
        is_verified = verify_signature_with_public_key(message_file, public_key)
    except ecdsa.MalformedPointError:
        print("Error: Invalid public key format.")
        return

    if is_verified:
        print("Digital signature is verified.")
    else:
        print("Digital signature is NOT verified.")
