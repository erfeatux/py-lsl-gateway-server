from fastapi.testclient import TestClient
from uuid import uuid4

from lslgwserver.routers import onLinkMessageRouter
from lslgwserver.models import LSLRequest
from lslgwlib.models import LinkMessage
from lslgwlib.enums import LinkNum


def test_linkmessage(app, data):
    # add router
    app.include_router(onLinkMessageRouter)

    # setup callback
    @onLinkMessageRouter.addCallback
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

    # test sender num
    reqData = LinkMessage(prim=1)
    resp = client.post("/lsl/linkmessage?sender=1", headers=data.headers, content="0¦¦")
    # callback was called at least once
    assert callback
    # status code - criterion for successful execution
    assert resp.status_code == 200

    # test sender num
    reqData = LinkMessage(prim=LinkNum.UNLINKED, num=-12)
    resp = client.post(
        "/lsl/linkmessage?sender=0", headers=data.headers, content="-12¦¦"
    )
    assert resp.status_code == 200

    # test str string
    reqData = LinkMessage(prim_num=0, str="teststring")
    resp = client.post(
        "/lsl/linkmessage?sender=0", headers=data.headers, content="0¦teststring¦"
    )
    assert resp.status_code == 200

    # test id as string
    reqData = LinkMessage(prim_num=4, id="teststring")
    resp = client.post(
        "/lsl/linkmessage?sender=4", headers=data.headers, content="0¦¦teststring"
    )
    assert resp.status_code == 200

    # test id as UUID
    uuid = uuid4()
    reqData = LinkMessage(prim_num=LinkNum.ROOT, id=uuid)
    resp = client.post(
        "/lsl/linkmessage?sender=1", headers=data.headers, content=f"0¦¦{uuid}"
    )
    assert resp.status_code == 200

    # invalid requests
    resp = client.post(
        "/lsl/linkmessage?sender=-1", headers=data.headers, content="0¦¦"
    )
    assert resp.status_code == 422
    resp = client.post(
        "/lsl/linkmessage?sender=256", headers=data.headers, content="0¦¦"
    )
    assert resp.status_code == 422
    resp = client.post("/lsl/linkmessage?sender=0", headers=data.headers, content="0¦")
    assert resp.status_code == 422
