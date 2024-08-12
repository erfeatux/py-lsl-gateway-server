from fastapi import APIRouter, Request
from dependency_injector.wiring import Provide
from typing import Callable, Coroutine
from logging import getLogger, Logger
from types import ModuleType
import asyncio

from lslgwserver.models import LSLRequest
from lslgwserver.auth import Container


# custom router class with callbacks
class Router(APIRouter):
    container = Container()
    __callbacks: list[Callable[[LSLRequest], bool | Coroutine]]
    __log: Logger

    def __init__(self, *args, **kwars) -> None:
        self.container.wire(modules=[__name__])
        self.__log = getLogger(self.__class__.__name__)
        self.__callbacks = list()
        super().__init__(*args, **kwars)

    def addCallback(self, cb: Callable[[LSLRequest], bool | Coroutine]) -> None:
        self.__callbacks.append(cb)

    async def call(self, *args, **kwars) -> bool:
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
