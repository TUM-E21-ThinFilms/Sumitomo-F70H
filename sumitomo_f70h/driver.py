# Copyright (C) 2016, see AUTHORS.md
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from slave.driver import Command
from slave.types import Float, String, Integer, Boolean, SingleType
from protocol import SumitomoF70HProtocol

class SumitomoF70HDriver(object):

    def __init__(self, transport, protocol=None):
        if protocol is None:
            protocol = SumitomoF70HProtocol()

        self._transport = transport
        self._protocol = protocol

    def _query(self, cmd, *data):
        if not isinstance(cmd, Command):
            raise TypeError("Can only query on Command")

        return cmd.query(self._transport, self._protocol, *data)

    def _write(self, cmd, *datas):
        if not isinstance(cmd, Command):
            cmd = Command(write=cmd)

        cmd.write(self._transport, self._protocol, *datas)

    def clear(self):
        self._protocol.clear(self._transport)

    def get_all_temperatures(self):
        cmd = Command(('$TEA',  [String, String, String, String]))
        return self._query(cmd, '')

    def get_temperature(self, id):
        if not id in [1,2,3,4]:
            raise ValueError("Unknown id")

        cmd = Command(('$TE' + str(id), String))
        return self._query(cmd, '')

    def get_all_pressures(self):
        cmd = Command(('$PRA', [String, String]))
        return self._query(cmd, '')

    def get_pressure(self, id):
        if not id in [1, 2]:
            raise ValueError("Unknown id")

        cmd = Command(('$PR' + str(id), String))
        return self._query(cmd, '')

    def turn_on(self):
        cmd = ('$ON1')
        self._write(cmd)

    def turn_off(self):
        cmd = ('$OFF')
        self._write(cmd)

    def reset(self):
        self._write(('$RS1'))

    def cold_head_run(self):
        self._write(('$CHR'))

    def cold_head_pause(self):
        self._write(('$CHP'))

    def cold_head_pause_off(self):
        self._write(('$POF'))

    def get_status(self):
        return self._query(Command(('$STA', String)))
