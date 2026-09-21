from ingest import load_documents
from chunker import split_documents

chunks = split_documents(load_documents())
bad = 0
for c in chunks:
       first = c.text.splitlines()[0]
       if len(c.text) < 100 or not first.startswith("THREAD:"):
           bad += 1
           print("FAIL", c.label, len(c.text), repr(first[:40]))
print(f"{len(chunks)} chunks, {bad} failing criterion 4")