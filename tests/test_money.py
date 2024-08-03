from fastapi.testclient import TestClient
from uuid import uuid4

from lslgwserver.routers import onMoneyRouter
from lslgwserver.models import LSLRequest
from lslgwlib.models import Avatar
from lslgwlib.models import Money


def test_linkmessage(app, data):
    # add router
    app.include_router(onMoneyRouter)

    # setup callback
    @onMoneyRouter.addCallback
    def testCallback(req: LSLRequest) -> bool:
        # callback variable - flag, set true when callback called
        global callback
        callback = True

        # test LSLRequest
        assert req.owner.modernName() == data.ownerName
        assert req.owner.id == data.ownerId
        assert req.objectName == data.objectName
        assert req.objectKey == data.objectId
        assert req.position == data.position
        assert req.rotation == data.rotation
        assert req.velocity == data.velocity
        assert str(req.region) == data.region
        assert req.production
        assert req.data == reqData
        return True

    client = TestClient(app)

    uuid = uuid4()
    # test sender num
    reqData = Money(amount=1, avatar=Avatar(uuid, "Test Name"))
    resp = client.post(
        "/lsl/money?money=1", headers=data.headers, content=f"{uuid}¦Test Name"
    )
    # callback was called at least once
    assert callback
    # status code - criterion for successful execution
    assert resp.status_code == 200

    # invalid data
    resp = client.post(
        "/lsl/money?money=-1", headers=data.headers, content=f"{uuid}¦Test Name"
    )
    assert resp.status_code == 422

    resp = client.post("/lsl/money?money=-", headers=data.headers, content=f"{uuid}")
    assert resp.status_code == 422
