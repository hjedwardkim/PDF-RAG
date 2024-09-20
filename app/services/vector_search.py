from app.services.database import get_db_connection


async def search_similar_chunks(query_embedding, limit=5):
    async with get_db_connection() as conn:
        results = await conn.fetch(
            """
            SELECT content FROM document_chunks
            ORDER BY embedding <=> $1
            LIMIT $2
            """,
            query_embedding,
            limit,
        )

    return [row["content"] for row in results]
