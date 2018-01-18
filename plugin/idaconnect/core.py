import logging

import ida_idp

from events.events_idp import *

logger = logging.getLogger("IDAConnect.Core")


class Hooks(object):

    def __init__(self, network):
        self._network = network

    def _send_event(self, event):
        self._network.send_event(event)


class IDPHooks(ida_idp.IDP_Hooks, Hooks):

    def __init__(self, network):
        ida_idp.IDP_Hooks.__init__(self)
        Hooks.__init__(self, network)

    def ev_undefine(self, ea):
        self._send_event(UndefinedEvent(ea))
        return 0


class IDBHooks(ida_idp.IDB_Hooks, Hooks):

    def __init__(self, network):
        ida_idp.IDB_Hooks.__init__(self)
        Hooks.__init__(self, network)


class Core(object):

    def __init__(self, plugin):
        super(Core, self).__init__()
        self._plugin = plugin

    def install(self):
        network = self._plugin.network
        self._idp_hooks = IDPHooks(network)
        self._idb_hooks = IDBHooks(network)

        logger.debug("Installing hooks")
        self._idp_hooks.hook()
        self._idb_hooks.hook()

    def uninstall(self):
        logger.debug("Uninstalling hooks")
        self._idp_hooks.unhook()
        self._idb_hooks.unhook()