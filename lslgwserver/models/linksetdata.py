from pydantic import BaseModel, Field

from lslgwserver.enums import LinksetDataAction


class LinksetData(BaseModel):
    action: LinksetDataAction = Field(frozen=True)
    key: str | None = Field(frozen=True)
    value: str | None = Field(frozen=True)
    keys: list[str] | None = Field(frozen=True)

    def __eq__(self, o):
        return all(
            (
                self.action == o.action,
                self.key == o.key,
                self.value == o.value,
                self.keys == o.keys,
            )
        )


class LinksetDataReset(LinksetData):
    action: LinksetDataAction = Field(
        default=LinksetDataAction.RESET,
        le=LinksetDataAction.RESET,
        ge=LinksetDataAction.RESET,
        frozen=True,
    )
    key: None = Field(default=None, frozen=True)
    value: None = Field(default=None, frozen=True)
    keys: None = Field(default=None, frozen=True)


class LinksetDataUpdate(LinksetData):
    action: LinksetDataAction = Field(
        default=LinksetDataAction.UPDATE,
        le=LinksetDataAction.UPDATE,
        ge=LinksetDataAction.UPDATE,
        frozen=True,
    )
    key: str = Field(frozen=True, min_length=1)
    value: str = Field(frozen=True, min_length=1)
    keys: None = Field(default=None, frozen=True)


class LinksetDataDelete(LinksetData):
    action: LinksetDataAction = Field(
        default=LinksetDataAction.DELETE,
        le=LinksetDataAction.MULTIDELETE,
        ge=LinksetDataAction.DELETE,
        frozen=True,
    )
    key: None = Field(default=None, frozen=True)
    value: None = Field(default=None, frozen=True)
    keys: list[str] = Field(frozen=True, min_length=1)
