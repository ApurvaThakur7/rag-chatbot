# test_utils.py

from scripts.utils import load_documents, split_text

for fname, text in load_documents("data/sample_docs/"):
    print(f"\n----- {fname} -----")
    chunks = split_text(text)
    print(f"{len(chunks)} chunks generated. First chunk:\n{chunks[0][:200]}...")
