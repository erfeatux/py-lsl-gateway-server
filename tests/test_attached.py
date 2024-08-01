from fastapi.testclient import TestClient
from uuid import uuid4

from lslgwserver.routers import onAttachRouter
from lslgwserver.models import LSLRequest


def test_channged(app, data):
    # add <changed> router
    app.include_router(onAttachRouter)
    avatarId = uuid4()

    # setup callback
    @onAttachRouter.addCallback
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
        assert req.data == avatarId
        return True

    client = TestClient(app)
    resp = client.post(f"/lsl/attached?avatarId={avatarId}", headers=data.headers)

    # callback was called at least once
    assert callback
    # status code - criterion for successful execution
    assert resp.status_code == 200

    # # invalid requests
    resp = client.post(
        "/lsl/attached?avatarId=00000000-0000-0000-0000-00000000000z",
        headers=data.headers,
    )
    assert resp.status_code == 422
