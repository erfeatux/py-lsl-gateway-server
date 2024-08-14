from fastapi import APIRouter, Request
from fastapi.responses import PlainTextResponse
from dependency_injector.wiring import Provide
from typing import Callable, Coroutine
from logging import getLogger, Logger
from types import ModuleType
import asyncio
import inspect

from lslgwserver.models import LSLRequest
from lslgwserver.auth import Container


# custom router class with callbacks
class Router(APIRouter):
    """FastAPI router"""

    # dependency-injector container
    container = Container()
    # callbacks
    __callbacks: list[Callable[[LSLRequest], bool | Coroutine]]
    __log: Logger

    def __init__(self, *args, **kwars) -> None:
        # wiring dependency-injector
        self.container.wire(modules=[__name__])
        self.__log = getLogger(self.__class__.__name__)
        self.__callbacks = list()
        super().__init__(*args, **kwars)

    def addCallback(self, cb: Callable[[LSLRequest], bool | Coroutine]) -> None:
        """Add callback"""
        self.__callbacks.append(cb)

    async def call(self, *args, **kwars) -> bool:
        """Call all registered callbacks"""
        results: list[bool] = list()
        coros: list[Coroutine] = list()

        for cb in self.__callbacks:
            res = cb(*args, **kwars)
            if isinstance(res, Coroutine):
                # async function? add to coroutines list
                coros.append(res)
            else:
                results.append(res)

        if len(coros):
            # run all callback coroutines
            corosResults = await asyncio.gather(*coros)
            # add coroutines results to res list
            for res in corosResults:
                if isinstance(res, bool):
                    results.append(res)
                else:
                    results.append(False)

        # False if any callable returns it
        return all(results)

    async def auth(self, req: Request, auth: ModuleType = Provide[Container.allow]):
        """Verify auth data"""
        # returns result of function call provided by dependency-injector
        return await auth.allowed(req)

    def wrap(self, func: Callable) -> Callable:
        """decorator"""

        async def wrapper(*args, **kwargs):
            # log
            log = getLogger(getattr(func, "__module__"))
            fargs = kwargs.copy()
            fargs.pop("req")
            log.debug(f"{fargs}")

            # auth
            if not await self.auth(kwargs["req"]):
                return PlainTextResponse(status_code=403)
            return await func(*args, **kwargs)

        # Fix signature of wrapper
        wrapper.__signature__ = inspect.Signature(
            parameters=[
                # Use all parameters from handler
                *inspect.signature(func).parameters.values(),
                # Skip *args and **kwargs from wrapper parameters:
                *filter(
                    lambda p: p.kind
                    not in (
                        inspect.Parameter.VAR_POSITIONAL,
                        inspect.Parameter.VAR_KEYWORD,
                    ),
                    inspect.signature(wrapper).parameters.values(),
                ),
            ],
            return_annotation=inspect.signature(func).return_annotation,
        )
        return wrapper
