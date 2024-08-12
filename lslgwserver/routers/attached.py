from fastapi.responses import PlainTextResponse
from fastapi import Request
from uuid import UUID

from .router import Router
from lslgwserver.models import LSLRequest


router = Router(prefix="/lsl", tags=["lsl"])


@router.post("/attached", response_class=PlainTextResponse)
async def attached(avatarId: UUID, req: Request) -> PlainTextResponse:
    if not await router.auth(req):
        return PlainTextResponse(status_code=403)
    # call all callbacks
    if await router.call(LSLRequest(req, avatarId)):
        return PlainTextResponse("Ok")
    return PlainTextResponse("Error", status_code=500)
