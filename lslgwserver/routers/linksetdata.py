from fastapi.responses import PlainTextResponse
from fastapi import Request
from pydantic import ValidationError

from .router import Router
from lslgwserver.models import LSLRequest
from lslgwserver.models.linksetdata import (
    LinksetData,
    LinksetDataReset,
    LinksetDataUpdate,
    LinksetDataDelete,
)
from lslgwserver.enums import LinksetDataAction


router = Router(prefix="/lsl", tags=["lsl"])


@router.post("/linksetdata", response_class=PlainTextResponse)
async def linksetdata(action: LinksetDataAction, req: Request) -> PlainTextResponse:
    # parse request data
    data: LinksetData
    try:
        match action:
            case LinksetDataAction.RESET:
                data = LinksetDataReset()
            case LinksetDataAction.UPDATE:
                body = await req.body()
                vals = body.decode("UTF-8").split(sep="¦", maxsplit=1)
                data = LinksetDataUpdate(key=vals[0], value=vals[1])
            case LinksetDataAction.DELETE:
                body = await req.body()
                if not len(body):
                    return PlainTextResponse("Empty body", status_code=422)
                data = LinksetDataDelete(
                    action=LinksetDataAction.DELETE, keys=[body.decode("UTF-8")]
                )
            case LinksetDataAction.MULTIDELETE:
                body = await req.body()
                if not len(body):
                    return PlainTextResponse("Empty body", status_code=422)
                vals = body.decode("UTF-8").split(sep=",", maxsplit=1)
                data = LinksetDataDelete(
                    action=LinksetDataAction.MULTIDELETE, keys=vals
                )
            case _:
                return PlainTextResponse(f"Invalid {action=}", status_code=422)
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
