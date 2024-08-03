from .linksetdata import router as onLinksetDataRouter
from .linkmessage import router as onLinkMessageRouter
from .chatmessage import router as onChatMessageRouter
from .attached import router as onAttachRouter
from .changed import router as onChangedRouter
from .money import router as onMoneyRouter
from .touch import router as onTouchRouter


__all__ = [
    "onChangedRouter",
    "onAttachRouter",
    "onLinksetDataRouter",
    "onLinkMessageRouter",
    "onChatMessageRouter",
    "onMoneyRouter",
    "onTouchRouter",
]
