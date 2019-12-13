import logging
import subprocess

from .wallet_adapter_base import WalletAdapterBase


class CMDAdapterException(Exception):
    def __init__(self, reason=None):
        self.reason = reason


class CMDAdapterResponse:

    def __init__(self, result, error, code):
        self.result = result
        self.error = error
        self.code = code


class CMDAdapter(WalletAdapterBase):

    def __init__(self, program_name):
        self.log = logging.getLogger('CMDAdapter')
        self.program_name = program_name

    def run(self, command, *args):
        try:
            proc = subprocess.Popen(self._build_args(
                command, *args), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            o, e = proc.communicate(timeout=10)
            return CMDAdapterResponse(o.decode('ascii').strip(), e.decode('ascii').strip(), proc.returncode)
        except Exception as e:
            message = 'Failed to run {} command'.format(command)
            self.log.error(message, e)
            raise CMDAdapterException(reason=message)

    def _build_args(self, command, *args):
        return [self.program_name, command, *args]