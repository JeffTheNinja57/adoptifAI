from fastapi import Security, HTTPException
from fastapi.security.api_key import APIKeyHeader
from sqlmodel import select
from app.main import SessionDep

from app.models.models import Shelter

api_key_header = APIKeyHeader(name="X-API-Key")


async def get_api_key(
        session: SessionDep,
        api_key: str = Security(api_key_header),
) -> Shelter:
    """Validate API key and return corresponding shelter"""
    shelter = session.exec(
        select(Shelter).where(Shelter.api_key == api_key)
    ).first()

    if not shelter:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )

    return shelter
