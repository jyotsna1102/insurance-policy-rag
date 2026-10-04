from rag.answer import generate_claim_answer, retrieve_context
from tests.test_extraction import extract_claim


claim = extract_claim()
query = " ".join(
	[
		diagnosis.name
		for diagnosis in claim.discharge_summary.diagnoses
	]
	+ claim.discharge_summary.procedures
)

context = retrieve_context(query)

answer = generate_claim_answer(claim, context)

print("\nANSWER:")
print(answer)