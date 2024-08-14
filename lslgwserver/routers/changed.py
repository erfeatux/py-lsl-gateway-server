from fastapi.responses import PlainTextResponse
from typing_extensions import Annotated
from pydantic import Field
from fastapi import Request

from .router import Router
from lslgwserver.models import LSLRequest


router = Router(prefix="/lsl", tags=["lsl"])


# https://wiki.secondlife.com/wiki/Changed
@router.post("/changed", response_class=PlainTextResponse)
@router.wrap
async def changed(
    change: Annotated[int, Field(gt=0, le=6143)],
    req: Request,
) -> PlainTextResponse:
    if await router.call(LSLRequest(req, change)):
        return PlainTextResponse("Ok")
    return PlainTextResponse("Error", status_code=500)
