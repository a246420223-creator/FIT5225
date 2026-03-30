import base64

with open("test_images/image_phone.jpeg", "rb") as f:
    encoded = base64.b64encode(f.read()).decode("utf-8")

with open("image_b64.txt", "w", encoding="utf-8") as f:
    f.write(encoded)

print("Saved to image_b64.txt")

