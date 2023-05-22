from digital_signature import main_generate_digital_signature, main_verify_digital_signature
from stegano import embed_message, extract_message

def main():
    print("What do you want to do?")
    print("1. Generate Stego Digitalized Painting")
    print("2. Verify Stego Digitalized Painting")
    input_main = -1
    while (input_main != 1 and input_main != 2):
        print("invalid input")
        input_main = int(input("Enter the main option: "))
    if input_main == 1:
        main_generate_digital_signature()
        original_image = input("Enter the image target: ")
        with open("message_with_signature.txt", "r") as file:
            message_content = file.read().strip()
        stego_image = embed_message(original_image, message_content)
        stego_image.save("result_image.png")

    elif input_main == 2:
        stego_image = input("Enter the stego image that want to extract: ")
        extracted_message = extract_message(stego_image)
        with open("extracted_message_from_image.txt", "w") as file:
            file.write(extracted_message)
        pubkey_file = input("Enter the public key file (.pem) : ")
        # message_file = input("Enter the message file (.txt) : ")
        main_verify_digital_signature(pubkey_file=pubkey_file, message_file="extracted_message_from_image.txt")

# Run the main function
if __name__ == "__main__":
    main()
# Example usage

# original_image = "/Users/ibnuhafizh/Documents/ITB/Semester8/kripto/Makalah 2/img/the_face.jpg"
# modified_image = embed_message(original_image, "Abil")
# modified_image.save("output_image.png")
# extracted_message = extract_message("/Users/ibnuhafizh/Documents/ITB/Semester8/kripto/Makalah 2/test/ori.png")
# print(extracted_message) # Output: "Hello, world!"
