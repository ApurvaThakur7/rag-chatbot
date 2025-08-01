# test_query.py
from scripts.query_engine import generate_answer_with_citations

query = "Which demographic group reported the highest number of burglary incidents between 2020 and 2024?"
response = generate_answer_with_citations(query)
print("\n💬 Answer:\n", response)
# "What are the criteria for conferring Bharat Ratna, Padma Vibhushan, Padma Bhushan, and Padma Shri?"