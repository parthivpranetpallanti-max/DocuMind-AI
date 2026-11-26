
import os
import shutil

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from document_processor import extract_pages, split_text

from vector_store import (
    initialize_index,
    add_documents,
    delete_document
)

from rag_pipeline import ask_question
from config import UPLOAD_DIR


# INITIALIZE FASTAPI
app = FastAPI(title="DocuMind AI")


# CORS CONFIGURATION
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# INITIALIZE FAISS
initialize_index()


# QUESTION MODEL
class Question(BaseModel):
    question: str


# HOME ROUTE
@app.get("/")
def home():
    return {
        "message": "DocuMind AI Backend Running Successfully"
    }


# UPLOAD DOCUMENT
@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    allowed = [".pdf", ".docx", ".txt"]

    filename = os.path.basename(file.filename or "")

    extension = os.path.splitext(filename)[1].lower()

    if extension not in allowed:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file format. Upload PDF, DOCX or TXT."
        )

    if not filename:
        raise HTTPException(
            status_code=400,
            detail="Invalid filename."
        )

    file_path = os.path.join(UPLOAD_DIR, filename)

    try:

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # EXTRACT DOCUMENT TEXT
        pages = extract_pages(file_path)

        # SPLIT TEXT INTO CHUNKS
        chunks = split_text(pages)

        # STORE EMBEDDINGS IN FAISS
        add_documents(chunks, filename)

        return {
            "message": "Document uploaded successfully",
            "filename": filename,
            "total_pages": len(pages),
            "total_chunks": len(chunks)
        }

    except HTTPException:
        raise

    except Exception as error:

        if os.path.exists(file_path):
            os.remove(file_path)

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )

    finally:
        await file.close()


# ASK QUESTIONS
@app.post("/ask")
def question_answer(data: Question):

    if not data.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )

    try:

        result = ask_question(data.question)

        return result

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# DELETE DOCUMENT
@app.delete("/document/{filename}")
def remove_document(filename: str):

    filename = os.path.basename(filename)

    file_path = os.path.join(UPLOAD_DIR, filename)

    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail="Document not found."
        )

    try:

        delete_document(filename)

        if os.path.exists(file_path):
            os.remove(file_path)

        return {
            "message": "Document deleted successfully",
            "filename": filename
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )
