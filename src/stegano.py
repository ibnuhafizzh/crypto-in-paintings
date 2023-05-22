from PIL import Image
from utils import binary_to_message, message_to_binary

END_OF_MESSAGE = message_to_binary("\n-----END OF MESSAGE-----")
def embed_message(image_file, message):
    """Embeds a message into an image using LSB steganography"""
    image = Image.open(image_file)
    pixels = list(image.getdata())
    binary_message = message_to_binary(message)
    if len(binary_message) > len(pixels):
        raise ValueError("Message is too long to embed in the image")
    binary_message += '0' * (len(pixels) - len(binary_message))
    modified_pixels = []
    message_index = 0
    for pixel in pixels:
        r, g, b = pixel
        if message_index < len(binary_message):
            r = (r & 0xFE) | int(binary_message[message_index])
            message_index += 1
        if message_index < len(binary_message):
            g = (g & 0xFE) | int(binary_message[message_index])
            message_index += 1
        if message_index < len(binary_message):
            b = (b & 0xFE) | int(binary_message[message_index])
            message_index += 1
        modified_pixels.append((r, g, b))
    modified_image = Image.new(image.mode, image.size)
    modified_image.putdata(modified_pixels)
    return modified_image

def extract_message(image_file):
    """Extracts a message from an image that was embedded using LSB steganography"""
    image = Image.open(image_file)
    pixels = list(image.getdata())
    binary_message = ''
    for pixel in pixels:
        r, g, b = pixel
        binary_message += str(r & 1)
        binary_message += str(g & 1)
        binary_message += str(b & 1)
        
    end_index = binary_message.find(END_OF_MESSAGE)
    # Trim the binary message to the expected length based on the number of pixels used to embed the message
    binary_message = binary_message[:end_index]
    # Convert the binary message back to the original message
    try:
        message = binary_to_message(binary_message)
    except:
        raise ValueError("Failed to decode the extracted binary message")
    return message