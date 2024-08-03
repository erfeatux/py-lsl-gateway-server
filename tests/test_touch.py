from fastapi.testclient import TestClient
from uuid import uuid4

from lslgwserver.routers import onTouchRouter
from lslgwserver.models import LSLRequest
from lslgwlib.models import Touch, Avatar


def test_touch(app, data):
    # add router
    app.include_router(onTouchRouter)

    # setup callback
    @onTouchRouter.addCallback
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

    # test valid touch event
    reqData = Touch(
        avatar=Avatar(uuid, "Test Name"),
        prim=1,
        face=0,
        startST=(0.1, 0.5),
        startUV=(0.11, 0.55),
        endST=(0.2, 0.9),
        endUV=(0.22, 0.99),
    )
    resp = client.post(
        "/lsl/touch",
        headers=data.headers,
        content=f"{uuid}¦Test Name¦1¦0¦0.1¦0.5¦0.11¦0.55¦0.2¦0.9¦0.22¦0.99",
    )
    # callback was called at least once
    assert callback
    # status code - criterion for successful execution
    assert resp.status_code == 200

    # invalid requests
    resp = client.post(
        "/lsl/touch",
        headers=data.headers,
        content=f"{uuid}¦Test Name Invalid¦1¦0¦0.1¦0.5¦0.11¦0.55¦0.2¦0.9¦0.22¦0.99",
    )
    assert resp.status_code == 422

    resp = client.post(
        "/lsl/touch",
        headers=data.headers,
        content=f"{uuid}¦Test Name¦256¦0¦0.1¦0.5¦0.11¦0.55¦0.2¦0.9¦0.22¦0.99",
    )
    assert resp.status_code == 422

    resp = client.post(
        "/lsl/touch",
        headers=data.headers,
        content=f"{uuid}¦Test Name¦1¦10¦0.1¦0.5¦0.11¦0.55¦0.2¦0.9¦0.22¦0.99",
    )
    assert resp.status_code == 422

    resp = client.post(
        "/lsl/touch",
        headers=data.headers,
        content=f"{uuid}¦Test Name¦1¦0¦-0.1¦0.5¦0.11¦0.55¦0.2¦0.9¦0.22¦0.99",
    )
    assert resp.status_code == 422

    resp = client.post(
        "/lsl/touch",
        headers=data.headers,
        content=f"{uuid}¦Test Name¦1¦0¦0.1¦0.5¦0.11¦0.55¦0.2¦0.9¦1.22¦0.99",
    )
    assert resp.status_code == 422
