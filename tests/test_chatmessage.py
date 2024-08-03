from fastapi.testclient import TestClient
from uuid import UUID

from lslgwserver.routers import onChatMessageRouter
from lslgwserver.models import LSLRequest
from lslgwlib.models import ChatMessage
from lslgwlib.enums import ChatChannel


def test_linkmessage(app, data):
    # add router
    app.include_router(onChatMessageRouter)

    # setup callback
    @onChatMessageRouter.addCallback
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
    reqData = ChatMessage(name="Test Name", message="testmessage")
    resp = client.post(
        "/lsl/chatmessage?channel=0",
        headers=data.headers,
        content=f"Test Name¦{UUID(int=0)}¦testmessage",
    )
    # callback was called at least once
    assert callback
    # status code - criterion for successful execution
    assert resp.status_code == 200

    reqData = ChatMessage(
        channel=ChatChannel.DEBUG, name="Test Name", message="testmessage"
    )
    resp = client.post(
        f"/lsl/chatmessage?channel={ChatChannel.DEBUG}",
        headers=data.headers,
        content=f"Test Name¦{UUID(int=0)}¦testmessage",
    )
    assert resp.status_code == 200

    # invalid requests
    resp = client.post(
        f"/lsl/chatmessage?channel={ChatChannel.DEBUG}",
        headers=data.headers,
        content=f"Test Name¦{UUID(int=0)}",
    )
    assert resp.status_code == 422
