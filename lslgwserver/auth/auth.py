from fastapi import Request


# empy auth function, works by default
# can replace by dependency-injector
async def allowed(req: Request) -> bool:
    return True
