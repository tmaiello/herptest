import virtualbox
import virtualbox.events
import virtualbox.library
from vix import VixHost, VixError, VixJob

class VmWrapper:
    def __init__(self, type, name, snapshot, ip, port, user, passwd):
        # Currently only supports VMWare and VirtualBox
        if type == "VMWare" or type == "VirtualBox":
            self._type = type
        else:
            # TODO - make this more robust
            print("Unsupported VM type!")
            return
        self._name = name
        self._snapshot = snapshot
        self._ip = ip
        self._port = port
        self._user = user
        self._passwd = passwd
    
    # TODO - do we need getters?
    @property
    def type(self):
        # Defines the type of VM
        return self._type
