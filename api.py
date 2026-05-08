from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
app = FastAPI()
class Numbers(BaseModel):
    values: list[float]
@app.post("/predict")
def predict(data: Numbers):
    df = pd.DataFrame({
        "value": data.values
    })
    df["lag1"] = df["value"].shift(1)
    df["roll3"] = df["value"].rolling(3).mean()
    last_row = df.iloc[-1]
    return {
        "last_value": float(last_row["value"]),
        "lag1": None if pd.isna(last_row["lag1"]) else float(last_row["lag1"]),
        "roll3": None if pd.isna(last_row["roll3"]) else float(last_row["roll3"])
    }