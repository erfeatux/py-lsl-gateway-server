from fastapi.testclient import TestClient

from lslgwserver.routers import onLinksetDataRouter
from lslgwserver.models import LSLRequest, LinksetData
from lslgwserver.enums import LinksetDataAction


def test_linkset(app, data):
    # add <changed> router
    app.include_router(onLinksetDataRouter)

    # setup callback
    @onLinksetDataRouter.addCallback
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

    # action - reset
    client = TestClient(app)
    reqData = LinksetData(
        action=LinksetDataAction.RESET, key=None, value=None, keys=None
    )
    resp = client.post("/lsl/linksetdata?action=0", headers=data.headers)
    # callback was called at least once
    assert callback
    # status code - criterion for successful execution
    assert resp.status_code == 200

    # action - update
    client = TestClient(app)
    reqData = LinksetData(
        action=LinksetDataAction.UPDATE, key="testkey", value="testvalue", keys=None
    )
    resp = client.post(
        "/lsl/linksetdata?action=1", headers=data.headers, content="testkey¦testvalue"
    )
    assert resp.status_code == 200

    # action - delete
    client = TestClient(app)
    reqData = LinksetData(
        action=LinksetDataAction.DELETE, key=None, value=None, keys=["testkey"]
    )
    resp = client.post(
        "/lsl/linksetdata?action=2", headers=data.headers, content="testkey"
    )
    assert resp.status_code == 200

    # action - delete milti
    client = TestClient(app)
    reqData = LinksetData(
        action=LinksetDataAction.MULTIDELETE,
        key=None,
        value=None,
        keys=["testkey0", "testkey1"],
    )
    resp = client.post(
        "/lsl/linksetdata?action=3", headers=data.headers, content="testkey0,testkey1"
    )
    assert resp.status_code == 200

    # invalid requests
    resp = client.post("/lsl/linksetdata?action=9", headers=data.headers)
    assert resp.status_code == 422

    resp = client.post("/lsl/linksetdata?action=1", headers=data.headers)
    assert resp.status_code == 422

    resp = client.post(
        "/lsl/linksetdata?action=1", headers=data.headers, content="testkey"
    )
    assert resp.status_code == 422

    resp = client.post(
        "/lsl/linksetdata?action=1", headers=data.headers, content="testkey¦"
    )
    assert resp.status_code == 422

    resp = client.post("/lsl/linksetdata?action=2", headers=data.headers)
    assert resp.status_code == 422

    resp = client.post("/lsl/linksetdata?action=3", headers=data.headers)
    assert resp.status_code == 422
