from fastapi import FastAPI, HTTPException
from fastapi.concurrency import run_in_threadpool

from app.schemas import PredictRequest, PredictResponse, AnnotateResponse, Box
from app.utils import decode_base64_image, encode_image_to_base64
from app.model import run_prediction

app = FastAPI(title="CloudEco Urban Waste Detection")


@app.get("/")
def root():
    return {"message": "CloudEco API is running"}


@app.post("/api/predict", response_model=PredictResponse)
async def predict(request: PredictRequest):
    try:
        image = decode_base64_image(request.image)
        result = await run_in_threadpool(run_prediction, image)

        detections = []
        boxes = []

        names = result.names
        for box in result.boxes:
            cls_id = int(box.cls[0].item())
            conf = float(box.conf[0].item())
            x1, y1, x2, y2 = box.xyxy[0].tolist()

            detections.append(names[cls_id])
            boxes.append(
                Box(
                    x=x1,
                    y=y1,
                    width=x2 - x1,
                    height=y2 - y1,
                    probability=conf
                )
            )

        speed = result.speed or {}

        return PredictResponse(
            uuid=request.uuid,
            count=len(detections),
            detections=detections,
            boxes=boxes,
            speed_preprocess_ms=float(speed.get("preprocess", 0.0)),
            speed_inference_ms=float(speed.get("inference", 0.0)),
            speed_postprocess_ms=float(speed.get("postprocess", 0.0)),
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/annotate", response_model=AnnotateResponse)
async def annotate(request: PredictRequest):
    try:
        image = decode_base64_image(request.image)
        result = await run_in_threadpool(run_prediction, image)
        annotated = result.plot()
        encoded = encode_image_to_base64(annotated)

        return AnnotateResponse(
            uuid=request.uuid,
            image=encoded
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))