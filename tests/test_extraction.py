from pathlib import Path

from claim.document_extraction import extract_document
from claim.schemas import Claim, DischargeSummary, HospitalBill


DATA_PATH = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "claim"
    / "sample_02"
)


def test_final_extraction():
    hospital_bill = extract_document(
        pdf_path=DATA_PATH / "Medical_Bill_2.pdf",
        schema=HospitalBill,
    )
    discharge_summary = extract_document(
        pdf_path=DATA_PATH / "Discharge_Summary_2.pdf",
        schema=DischargeSummary,
    )
    claim = Claim(
        discharge_summary=discharge_summary,
        hospital_bill=hospital_bill,
    )

    print("\n===== EXTRACTED CLAIM =====\n")

    print(claim)

    print("\n===== AS JSON =====\n")

    print(claim.model_dump_json(indent=2))

test_final_extraction()