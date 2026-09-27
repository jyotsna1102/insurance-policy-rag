from datetime import date
from typing import List

from pydantic import BaseModel, Field


class Diagnosis(BaseModel):
    name: str
    primary: bool = False


class DischargeSummary(BaseModel):
    diagnoses: List[Diagnosis]
    procedures: List[str] = Field(
        default_factory=list,
        description=(
            "Explicitly documented diagnostic tests, treatments, procedures, "
            "or supportive care provided during the hospitalization."
        ),
    )

    admission_date: date
    discharge_date: date

    hospitalization_days: int | None = None


class BillItem(BaseModel):
    description: str
    amount: float


class HospitalBill(BaseModel):
    currency: str = "INR"
    gross_total_amount: float | None = Field(
        default=None,
        description="Total of all bill items before deposits or deductions.",
    )
    deposit_amount: float = Field(
        default=0,
        description="Deposit or advance payment deducted from the bill.",
    )
    total_amount: float = Field(
        description="Net amount payable after deposits or deductions.",
    )

    items: List[BillItem] = Field(default_factory=list)


class Claim(BaseModel):
    discharge_summary: DischargeSummary
    hospital_bill: HospitalBill