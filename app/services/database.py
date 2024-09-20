from typing import Dict, List

import asyncpg

from app.config import settings


async def get_db_connection():
    return await asyncpg.connect(
        user=settings.postgres_user,
        password=settings.postgres_password,
        database=settings.postgres_db,
        host=settings.db_host,
        port=settings.db_port,
    )


async def init_db():
    conn = await get_db_connection()
    try:
        await conn.execute("CREATE EXTENSION IF NOT EXISTS vector;")

        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS document_chunks (
                id SERIAL PRIMARY KEY,
                filename TEXT,
                content TEXT,
                embedding vector(1536)
            );
        """
        )

    finally:
        await conn.close()


async def insert_document_chunks(
    filename: str, chunks: List[str], embeddings: List[List[float]]
):
    conn = await get_db_connection()
    try:
        formatted_data = [
            (filename, chunk, f"[{','.join(map(str, embedding))}]")
            for chunk, embedding in zip(chunks, embeddings)
        ]

        await conn.executemany(
            """
            INSERT INTO document_chunks (filename, content, embedding)
            VALUES ($1, $2, $3::vector)
        """,
            formatted_data,
        )

    finally:
        await conn.close()


async def get_document_count() -> int:
    conn = await get_db_connection()
    try:
        result = await conn.fetchval("SELECT COUNT(*) FROM document_chunks")
        return result

    finally:
        await conn.close()


async def get_document_filenames(limit: int = 20) -> List[Dict]:
    conn = await get_db_connection()
    try:
        rows = await conn.fetch(
            """
            SELECT id, filename, content, embedding
            FROM document_chunks
            LIMIT $1
        """,
            limit,
        )
        return [row["filename"] for row in rows]

    finally:
        await conn.close()


async def search_similar_documents(
    query_embedding: List[float], limit: int = 10
) -> List[Dict]:
    conn = await get_db_connection()
    try:
        query_embedding_formatted = f"[{','.join(map(str, query_embedding))}]"

        rows = await conn.fetch(
            """
            SELECT id, filename, content, embedding <=> $1::vector AS distance
            FROM document_chunks
            ORDER BY distance
            LIMIT $2
        """,
            query_embedding_formatted,
            limit,
        )

        return [dict(row) for row in rows]

    finally:
        await conn.close()
