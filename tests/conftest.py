import pytest
from uuid import UUID, uuid4
from fastapi import FastAPI
from pydantic import BaseModel


__app = FastAPI()


class TestData(BaseModel):
    ownerId: UUID = uuid4()
    ownerName: str = "testname.resident"
    objectId: UUID = uuid4()
    objectName: str = "Test object name"
    position: tuple[float, float, float] = (50.362698, 39.342766, 1000.523254)
    rotation: tuple[float, float, float, float] = (0.0, 0.0, 0.0, 1.0)
    velocity: tuple[float, float, float] = (0.0, 0.0, 0.0)
    region: str = "Region Name (256, 512)"

    @property
    def headers(self) -> dict[str, str]:
        return {
            "X-SecondLife-Owner-Key": str(self.ownerId),
            "X-SecondLife-Owner-Name": self.ownerName,
            "X-SecondLife-Object-Key": str(self.objectId),
            "X-SecondLife-Object-Name": self.objectName,
            "X-SecondLife-Local-Position": str(self.position),
            "X-SecondLife-Local-Rotation": str(self.rotation),
            "X-SecondLife-Local-Velocity": str(self.velocity),
            "X-SecondLife-Region": self.region,
            "X-SecondLife-Shard": "Production",
            "Date": "Mon, 29 Jul 2024 18:38:38 GMT",
            "Server": "Second Life LSL/Second Life Server 2024-06-11.9458617693 (http://secondlife.com)",
            "X-LL-Request-Id": "ZqfhrjJAbH10OU82a__e-AAAATE",
        }


@pytest.fixture(scope="session")
def app() -> FastAPI:
    return __app


@pytest.fixture
def data() -> TestData:
    return TestData()
