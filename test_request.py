import base64
import requests

with open("test_images/image_phone.jpeg", "rb") as f:
    image_b64 = base64.b64encode(f.read()).decode("utf-8")

payload = {
    "uuid": "test-123",
    "image": image_b64
}

response = requests.post("http://127.0.0.1:8000/api/predict", json=payload)

print("Status:", response.status_code)
print(response.json())