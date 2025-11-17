from fastapi import APIRouter, HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT

from ..schemas.pairs import PairStatus, TrackedPair, TrackedPairCreate
from ..store import PairAlreadyTracked, PairNotFound, store

router = APIRouter(prefix="/api/pairs", tags=["pairs"])



@router.post("", response_model=TrackedPair, status_code=HTTP_201_CREATED)
async def create_pair(payload: TrackedPairCreate) -> TrackedPair:
    try:
        return store.add_pair(payload)
    except PairAlreadyTracked as exc:
        raise HTTPException(status_code=HTTP_409_CONFLICT, detail=str(exc))


@router.get("", response_model=list[TrackedPair])
async def list_pairs(status: PairStatus | None = None) -> list[TrackedPair]:
    return store.list_pairs(status=status)


@router.delete(
    "/{coin_id}/{vs_currency}",
    response_model=TrackedPair,
    status_code=HTTP_201_CREATED,
)
async def stop_pair(coin_id: str, vs_currency: str) -> TrackedPair:
    try:
        return store.stop_pair(coin_id, vs_currency)
    except PairNotFound as exc:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(exc))

