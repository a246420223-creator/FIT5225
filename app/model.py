from ultralytics import YOLO

model = YOLO("models/best_model.pt")


def run_prediction(image):
    results = model.predict(image, verbose=False)
    return results[0]