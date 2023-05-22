def message_to_binary(message):
    """Converts a message string into binary format"""
    return ''.join(format(ord(c), '08b') for c in message)

def binary_to_message(binary):
    """Converts a binary string back into the original message"""
    return ''.join(chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8))