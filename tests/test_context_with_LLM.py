from rag.answer import retrieve_context, generate_answer



query = "What is the maternity benefit limit?"

context = retrieve_context(query)

answer = generate_answer(query, context)

print("\nANSWER:")
print(answer)