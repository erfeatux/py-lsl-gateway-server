from pydantic import BaseModel
from fastapi import Request
from uuid import UUID
import re

from lslgwlib.models import HTTPData, Avatar, Region


# LSL request model
class LSLRequest(HTTPData):
    def __init__(self, *args, **kwargs) -> None:
        # constructor by http request and parsed data
        if (
            len(args) == 2
            and isinstance(args[0], Request)
            and isinstance(args[1], BaseModel | list | int | float | str)
        ):
            headers: dict[str, str] = dict()
            for headName in args[0].headers:
                if not headName.startswith("x-secondlife"):
                    headers[headName] = args[0].headers[headName]
            super().__init__(
                owner=Avatar(
                    args[0].headers["X-SecondLife-Owner-Key"],
                    args[0].headers["X-SecondLife-Owner-Name"],
                ),
                objectKey=UUID(args[0].headers["X-SecondLife-Object-Key"]),
                objectName=args[0].headers["X-SecondLife-Object-Name"],
                position=re.sub(
                    r"(\(|\))", "", args[0].headers["X-SecondLife-Local-Position"]
                ).split(","),
                rotation=re.sub(
                    r"(\(|\))", "", args[0].headers["X-SecondLife-Local-Rotation"]
                ).split(","),
                velocity=re.sub(
                    r"(\(|\))", "", args[0].headers["X-SecondLife-Local-Velocity"]
                ).split(","),
                region=Region(args[0].headers["X-SecondLife-Region"]),
                production=args[0].headers["X-SecondLife-Shard"] == "Production",
                data=args[1],
                headers=headers,
            )
        else:
            super().__init__(**kwargs)
