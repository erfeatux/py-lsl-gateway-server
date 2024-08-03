from fastapi.responses import PlainTextResponse
from fastapi import Request
from pydantic import ValidationError

from .router import Router
from lslgwserver.models import LSLRequest
from lslgwlib.models import Touch, Avatar


router = Router(prefix="/lsl", tags=["lsl"])


@router.post("/touch", response_class=PlainTextResponse)
async def touch(req: Request) -> PlainTextResponse:
    # parse request data
    data: Touch
    body = await req.body()
    vals = body.decode("UTF-8").split(sep="¦", maxsplit=11)
    try:
        data = Touch(
            avatar=Avatar(vals[0], vals[1]),
            prim=vals[2],
            face=vals[3],
            startST=(vals[4], vals[5]),
            startUV=(vals[6], vals[7]),
            endST=(vals[8], vals[9]),
            endUV=(vals[10], vals[11]),
        )
    except ValidationError as exception:
        return PlainTextResponse(f"{exception=}", status_code=422)
    except IndexError as exception:
        return PlainTextResponse(
            f"Request body must contains 12 entries, but has {len(vals)}\n{vals=}\n{exception=}",
            status_code=422,
        )

    # call all callbacks
    if await router.call(LSLRequest(req, data)):
        return PlainTextResponse("Ok")
    return PlainTextResponse("Error", status_code=500)
