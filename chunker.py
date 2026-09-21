"""
Stage 2 of the pipeline: splitting documents into chunks.

`fallback_split` is the starter's original fixed-window chunker, kept for
comparison. `split_documents` is my thread-aware replacement: one thread per
chunk, split at reply boundaries only when a thread is too long, with the
THREAD: title repeated on every piece.
"""

import re
from dataclasses import dataclass

import config
from ingest import Document

MAX_CHARS = 1200   # a thread longer than this gets split at reply boundaries
MIN_CHARS = 100    # anything shorter merges into its neighbour


@dataclass
class Chunk:
    """One piece of one document."""

    text: str
    source: str        # which file it came from
    index: int         # which chunk within that file, starting at 0
    produced_by: str   # the function that made it — cite this in your README

    @property
    def label(self) -> str:
        return f"{self.source}#{self.index}"


def fallback_split(
    documents: list[Document],
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[Chunk]:
    """
    The starter's original chunker. Fixed-size character windows with overlap.

    Keep this function. Milestone 3's stop rule points back at it, and having
    something to compare your own strategy against is useful in unit 2.
    """
    chunk_size = chunk_size or config.CHUNK_SIZE
    overlap = overlap or config.CHUNK_OVERLAP

    if overlap >= chunk_size:
        raise ValueError("overlap has to be smaller than chunk_size")

    chunks: list[Chunk] = []
    for doc in documents:
        start = 0
        index = 0
        while start < len(doc.text):
            piece = doc.text[start : start + chunk_size].strip()
            if piece:
                chunks.append(
                    Chunk(
                        text=piece,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::fallback_split",
                    )
                )
                index += 1
            start += chunk_size - overlap

    return chunks


def _render(title: str, replies: list[str]) -> str:
    return "\n\n".join([title] + replies) if title else "\n\n".join(replies)


def _pack(title: str, pieces: list[str], max_chars: int) -> list[str]:
    """Greedily pack pieces into chunks. When a chunk overflows, the title is
    repeated on the next one and the last piece carries over as overlap."""
    out: list[str] = []
    current: list[str] = []
    for piece in pieces:
        if current and len(_render(title, current + [piece])) > max_chars:
            out.append(_render(title, current))
            current = [current[-1], piece]
        else:
            current = current + [piece]
    if current:
        out.append(_render(title, current))
    return out


def split_documents(documents: list[Document]) -> list[Chunk]:
    """Thread-aware chunker: one thread per chunk, split only when too long."""
    chunks: list[Chunk] = []
    for doc in documents:
        text = doc.text.strip()
        if not text:
            continue

        if text.startswith("THREAD:"):
            title, _, body = text.partition("\n")
            title = title.strip()
            pieces = [
                p.strip()
                for p in re.split(r"(?m)^(?=--- reply )", body)
                if p.strip()
            ]
        else:  # not a thread: pack paragraphs instead
            title = ""
            pieces = [p.strip() for p in text.split("\n\n") if p.strip()]

        texts = _pack(title, pieces, MAX_CHARS) if pieces else [text]

        # merge fragments shorter than MIN_CHARS into the previous chunk
        merged: list[str] = []
        for t in texts:
            if merged and len(t) < MIN_CHARS:
                merged[-1] += "\n\n" + t
            else:
                merged.append(t)

        for i, t in enumerate(merged):
            chunks.append(
                Chunk(
                    text=t,
                    source=doc.source,
                    index=i,
                    produced_by="chunker.py::split_documents",
                )
            )
    return chunks


def describe(chunks: list[Chunk]) -> str:
    """A one-line summary, printed after indexing."""
    if not chunks:
        return "0 chunks"
    lengths = [len(c.text) for c in chunks]
    return (
        f"{len(chunks)} chunks, "
        f"{sum(lengths) // len(lengths)} characters on average "
        f"(shortest {min(lengths)}, longest {max(lengths)}), "
        f"produced by {chunks[0].produced_by}"
    )


if __name__ == "__main__":
    from ingest import load_documents

    chunks = split_documents(load_documents())
    print(describe(chunks))