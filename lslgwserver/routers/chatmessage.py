from fastapi.responses import PlainTextResponse
from fastapi import Request

from .router import Router
from lslgwserver.models import LSLRequest
from lslgwlib.models import ChatMessage


router = Router(prefix="/lsl", tags=["lsl"])


@router.post("/chatmessage", response_class=PlainTextResponse)
async def linkmessage(channel: int, req: Request) -> PlainTextResponse:
    # parse request data
    data: ChatMessage
    body = await req.body()
    vals = body.decode("UTF-8").split(sep="¦", maxsplit=2)
    data = ChatMessage(channel=channel, name=vals[0], id=vals[1], message=vals[2])

    # call all callbacks
    if await router.call(LSLRequest(req, data)):
        return PlainTextResponse("Ok")
    return PlainTextResponse("Error", status_code=500)
