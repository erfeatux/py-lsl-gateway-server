from dependency_injector import containers, providers

from . import auth


class Container(containers.DeclarativeContainer):
    allow = providers.Object(auth)
