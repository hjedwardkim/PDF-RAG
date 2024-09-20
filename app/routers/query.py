from fastapi import APIRouter

from app.models.schemas import QueryRequest, QueryResponse
from app.services.database import (
    get_document_count,
    get_document_filenames,
    search_similar_documents,
)
from app.services.embedding_service import generate_query_embedding
from app.services.llm_service import generate_answer

router = APIRouter()


@router.post("/query", response_model=QueryResponse)
async def search(query: QueryRequest):
    query_embedding = await generate_query_embedding(query.question)
    similar_docs = await search_similar_documents(query_embedding)

    context = "\n".join([doc["content"] for doc in similar_docs])
    answer = generate_answer(query.question, context)

    return QueryResponse(answer=answer)


@router.get("/document_count")
async def document_count():
    count = await get_document_count()

    return {"document_count": count}


@router.get("/document_names")
async def sample_documents(limit: int = 5):
    filenames = await get_document_filenames(limit)

    return {"document_names": filenames}
