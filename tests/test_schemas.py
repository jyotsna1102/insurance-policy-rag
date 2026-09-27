from claim.schemas import (
    Diagnosis,
    DischargeSummary,
    BillItem,
    HospitalBill,
    Claim,
)


def test_claim_schema():

    discharge_summary = DischargeSummary(
        diagnoses=[
            Diagnosis(
                name="Acute gastroenteritis with dehydration",
                primary=True
            )
        ],
        procedures=[
            "IV fluid therapy and medications",
            "Laboratory tests",
            "Nursing support"
        ],
        admission_date="2026-09-26",
        discharge_date="2026-09-30",
        hospitalization_days=5
    )

    hospital_bill = HospitalBill(
        currency="INR",
        total_amount=20060.00,
        items=[
            BillItem(
                description="Consultation - Senior Consultant Internal Medicine",
                amount=1500.00
            ),
            BillItem(
                description="Private Room Charges (AC)",
                amount=10000.00
            ),
            BillItem(
                description="IV Fluid Therapy & Medications",
                amount=3200.00
            ),
            BillItem(
                description="Laboratory Tests",
                amount=1800.00
            ),
            BillItem(
                description="Nursing Care",
                amount=500.00
            )
        ]
    )

    claim = Claim(
        discharge_summary=discharge_summary,
        hospital_bill=hospital_bill
    )

    print(claim)

test_claim_schema()