from fastapi import APIRouter, File, UploadFile

from app.models.schemas import UpsertResponse
from app.services.database import insert_document_chunks
from app.services.embedding_service import generate_embeddings
from app.services.pdf_parser import parse_pdf

router = APIRouter()


@router.post("/upsert", response_model=UpsertResponse)
async def upsert_document(file: UploadFile = File(...)):
    content = await file.read()
    chunks = parse_pdf(content)
    embeddings = await generate_embeddings(chunks)
    await insert_document_chunks(file.filename, chunks, embeddings)

    return {"message": "Document uploaded and processed successfully"}
