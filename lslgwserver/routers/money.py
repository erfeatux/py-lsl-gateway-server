from fastapi.responses import PlainTextResponse
from fastapi import Request
from typing_extensions import Annotated
from pydantic import Field

from .router import Router
from lslgwserver.models import LSLRequest
from lslgwlib.models import Avatar
from lslgwlib.models import Money


router = Router(prefix="/lsl", tags=["lsl"])


@router.post("/money", response_class=PlainTextResponse)
async def money(
    money: Annotated[int, Field(ge=0, le=0x7FFFFFFF)],
    req: Request,
) -> PlainTextResponse:
    # parse request data
    data: Money
    body = await req.body()
    vals = body.decode("UTF-8").split(sep="¦", maxsplit=1)
    data = Money(amount=money, avatar=Avatar(vals[0], vals[1]))

    # call all callbacks
    if await router.call(LSLRequest(req, data)):
        return PlainTextResponse("Ok")
    return PlainTextResponse("Error", status_code=500)
