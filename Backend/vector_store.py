import faiss
import numpy as np
import pickle
import os

from embedding_service import generate_embedding
from config import STORAGE_DIR


INDEX_PATH = os.path.join(STORAGE_DIR, "faiss.index")

METADATA_PATH = os.path.join(STORAGE_DIR, "metadata.pkl")


index = None

metadata = []


def save_index():

    if index is not None:

        faiss.write_index(index, INDEX_PATH)

    elif os.path.exists(INDEX_PATH):

        os.remove(INDEX_PATH)

    with open(METADATA_PATH, "wb") as file:

        pickle.dump(metadata, file)


def initialize_index():

    global index, metadata

    if os.path.exists(INDEX_PATH):

        index = faiss.read_index(INDEX_PATH)

    if os.path.exists(METADATA_PATH):

        with open(METADATA_PATH, "rb") as file:

            metadata = pickle.load(file)


def add_documents(chunks, document_name):

    global index, metadata

    if not chunks:

        raise ValueError("No text chunks to index")

    embeddings = []

    new_metadata = []

    for chunk_id, chunk in enumerate(chunks):

        vector = generate_embedding(chunk["text"])

        embeddings.append(vector)

        new_metadata.append({

            "document": document_name,

            "chunk_id": chunk_id,

            "page": chunk["page"],

            "text": chunk["text"]

        })

    vectors = np.array(embeddings, dtype="float32")

    faiss.normalize_L2(vectors)

    if index is None:

        dimension = vectors.shape[1]

        index = faiss.IndexFlatIP(dimension)

    index.add(vectors)

    metadata.extend(new_metadata)

    save_index()


def search_documents(question, top_k=5):

    if index is None or index.ntotal == 0:

        return []

    question_vector = np.array(

        [generate_embedding(question)],

        dtype="float32"

    )

    faiss.normalize_L2(question_vector)

    scores, indices = index.search(

        question_vector,

        min(top_k, index.ntotal)

    )

    results = []

    for score, idx in zip(scores[0], indices[0]):

        if idx == -1:

            continue

        result = metadata[idx].copy()

        result["similarity"] = float(score)

        results.append(result)

    return results


def delete_document(document_name):

    global index, metadata

    remaining = [

        item for item in metadata

        if item["document"] != document_name

    ]

    index = None

    metadata = []

    if remaining:

        embeddings = [

            generate_embedding(item["text"])

            for item in remaining

        ]

        vectors = np.array(embeddings, dtype="float32")

        faiss.normalize_L2(vectors)

        index = faiss.IndexFlatIP(vectors.shape[1])

        index.add(vectors)

        metadata = remaining

    save_index()