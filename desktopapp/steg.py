from PIL import Image
import random

def to_binary(data):
    return ''.join(format(byte, '08b') for byte in data)

def hide_data_random(input_image, output_image, data, key):
    img = Image.open(input_image)
    encoded = img.copy()
    data += "<<<END>>>"
    binary_data = to_binary(data.encode())
    pixels = [(x, y) for x in range(img.width) for y in range(img.height)]
    
    random.seed(key)  # randomize based on key
    random.shuffle(pixels)
    
    idx = 0
    for x, y in pixels:
        pixel = list(img.getpixel((x, y)))
        for i in range(3):
            if idx < len(binary_data):
                pixel[i] = pixel[i] & ~1 | int(binary_data[idx])
                idx += 1
        encoded.putpixel((x, y), tuple(pixel))
        if idx >= len(binary_data):
            encoded.save(output_image)
            return

def extract_data_random(image_path, key):
    img = Image.open(image_path)
    binary_data = ""
    pixels = [(x, y) for x in range(img.width) for y in range(img.height)]
    
    random.seed(key)
    random.shuffle(pixels)
    
    for x, y in pixels:
        pixel = img.getpixel((x, y))
        for i in range(3):
            binary_data += str(pixel[i] & 1)
    bytes_list = []
    for i in range(0, len(binary_data), 8):
        byte = binary_data[i:i+8]
        if len(byte) == 8:
            bytes_list.append(int(byte, 2))
    decoded = bytearray(bytes_list).decode(errors="ignore")
    if "<<<END>>>" in decoded:
        decoded = decoded.split("<<<END>>>")[0]
    else:
        return None
    return decoded.strip()
