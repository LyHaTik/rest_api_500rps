from fastapi import FastAPI
from pydantic import BaseModel
from typing import Literal

from pick_regno import pick_regno


app = FastAPI()

model_name = "micromodel.cbm"


class Record(BaseModel):
    regno_recognize: str
    afts_regno_ai: str
    recognition_accuracy: float
    afts_regno_ai_score: float
    afts_regno_ai_char_scores: str
    afts_regno_ai_length_scores: str
    camera_type: str
    camera_class: str
    time_check: str
    direction: Literal['0', '1']


@app.post("/predict")
def predict(record: Record):
    probs = pick_regno(
        camera_regno=record.regno_recognize,
        nn_regno=record.afts_regno_ai,
        camera_score=record.recognition_accuracy,
        nn_score=record.afts_regno_ai_score,
        nn_sym_scores=record.afts_regno_ai_char_scores,
        nn_len_scores=record.afts_regno_ai_length_scores,
        camera_type=record.camera_type,
        camera_class=record.camera_class,
        time_check=record.time_check,
        direction=record.direction,
        model_name=model_name
    )
    return {"result": probs.tolist()}
