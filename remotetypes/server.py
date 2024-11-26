# server.py

import logging
import sys
import Ice

from remotetypes.factory import Factory

class Server(Ice.Application):
    """Ice.Application para el servidor."""

    def __init__(self) -> None:
        """Inicializa los objetos del servidor."""
        super().__init__()
        self.logger = logging.getLogger(__name__)

    def run(self, args: list[str]) -> int:
        """Ejecuta las acciones principales del servidor."""
        properties = self.communicator().getProperties()
        persistence_dir = properties.getProperty('Persistence.Directory') or 'data'

        adapter = self.communicator().createObjectAdapter("remotetypes")
        factory_servant = Factory(adapter, persistence_dir)
        proxy = adapter.add(factory_servant, self.communicator().stringToIdentity("Factory"))
        print(f"Factory is running at: {proxy}")

        adapter.activate()
        self.shutdownOnInterrupt()
        self.communicator().waitForShutdown()
        return 0

if __name__ == '__main__':
    sys.exit(Server().main(sys.argv))
