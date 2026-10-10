
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class LiverRiskRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    Age: int = Field(ge=1, le=120)
    Gender: Literal["Male", "Female"]
    TB: float = Field(gt=0, le=1000)
    DB: float = Field(gt=0, le=500)
    Alkphos: float = Field(gt=0, le=10000)
    Sgpt: float = Field(ge=0, le=10000)
    Sgot: float = Field(ge=0, le=10000)
    TP: float = Field(gt=0, le=30)
    ALB: float = Field(gt=0, le=20)
    A_G_Ratio: float = Field(gt=0, le=10)

    @field_validator("Gender", mode="before")
    @classmethod
    def normalize_gender(cls, value):
        if isinstance(value, str):
            return value.strip().title()
        return value

    def model_features(self):
        return {
            "Age": self.Age,
            "Gender": self.Gender,
            "TB": self.TB,
            "DB": self.DB,
            "Alkphos": self.Alkphos,
            "Sgpt": self.Sgpt,
            "Sgot": self.Sgot,
            "TP": self.TP,
            "ALB": self.ALB,
            "A/G Ratio": self.A_G_Ratio,
        }
