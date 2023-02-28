

from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from app.model import predict_pipeline

app = FastAPI()


class TextIn(BaseModel):
    danceability : float
    energy :float
    key : int
    loudness : float
    mode : int
    speechiness : float
    acousticness : float
    instrumentalness :float
    liveness : float
    valence : float
    tempo : float
    type : str
    duration_ms : float
    time_signature : int


class PredictionOut(BaseModel):
    popularity: float

# @app.post("/predict", response_model=PredictionOut)
@app.post("/predict")
def predict(item: TextIn ):

    values = [x for x in item.__dict__.values()]
    popularity = predict_pipeline(
        values
    )
    return {'popularity':popularity}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=6000)