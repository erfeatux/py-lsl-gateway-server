from fastapi import APIRouter
from typing import Callable, Coroutine
import asyncio

from lslgwserver.models import LSLRequest


# custom router class with callbacks
class Router(APIRouter):
    __callbacks: list[Callable[[LSLRequest], bool | Coroutine]]

    def __init__(self, *args, **kwars) -> None:
        self.__callbacks = list()
        super().__init__(*args, **kwars)

    # def addCallback(self, cb: Callable[P, R]) -> None:
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
