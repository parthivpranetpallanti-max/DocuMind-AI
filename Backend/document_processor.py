import os

from pypdf import PdfReader
from docx import Document

from config import CHUNK_SIZE, CHUNK_OVERLAP


def extract_pages(file_path):

    extension = os.path.splitext(file_path)[1].lower()

    pages = []

    # PDF PROCESSING
    if extension == ".pdf":

        reader = PdfReader(file_path)

        for page_number, page in enumerate(reader.pages):

            text = page.extract_text() or ""

            if text.strip():

                pages.append({

                    "page": page_number + 1,

                    "text": text

                })

    # WORD DOCUMENT PROCESSING
    elif extension == ".docx":

        doc = Document(file_path)

        text = "\n".join(

            paragraph.text

            for paragraph in doc.paragraphs

        )

        if text.strip():

            pages.append({

                "page": 1,

                "text": text

            })

    # TEXT FILE PROCESSING
    elif extension == ".txt":

        with open(file_path, "r", encoding="utf-8") as file:

            text = file.read()

        if text.strip():

            pages.append({

                "page": 1,

                "text": text

            })

    else:

        raise ValueError("Unsupported file format")

    if not pages:

        raise ValueError(
            "No readable text found in document."
        )

    return pages


def split_text(pages):

    chunks = []

    for page_data in pages:

        text = page_data["text"]

        start = 0

        while start < len(text):

            end = start + CHUNK_SIZE

            chunk = text[start:end].strip()

            if chunk:

                chunks.append({

                    "text": chunk,

                    "page": page_data["page"]

                })

            start += CHUNK_SIZE - CHUNK_OVERLAP

    return chunks