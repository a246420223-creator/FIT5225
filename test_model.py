from ultralytics import YOLO

# load your trained model
model = YOLO("models/best_model.pt")

# run prediction on test image
results = model("test_images/image_phone.jpeg")

# print results
print(results)