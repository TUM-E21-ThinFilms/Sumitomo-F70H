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

import slave
import logging

from slave.protocol import Protocol
from slave.transport import Timeout

class CommunicationError(Exception):
    pass

class SumitomoF70HProtocol(Protocol):
    def __init__(self, terminal="\r", separator=',', encoding='ascii', logger=None):

        if logger is None:
            logger = logging.getLogger(__name__)
            logger.addHandler(logging.NullHandler())

        self.terminal = terminal
        self.separator = separator
        self.logger = logger
        self.encoding = encoding

    def clear(self, transport):
        try:
            while True:
                transport.read_bytes(5)
        except slave.transport.Timeout:
            return

    def set_logger(self, logger):
        self.logger = logger

    def compute_checksum(self, data):
        crcmask = 0xA001
        i = 0
        l = 0
        crc = 0xFFFF
        while l < len(data):
            crc = (0x0000 | (data[l] & 0xFF)) ^ crc
            while (i < 8):
                lsb = crc & 0x1
                crc = crc >> 1
                if lsb == 1:
                    crc = crc ^ crcmask
                i = i + 1
            i = 0
            l = l + 1
        return crc

    def create_message(self, header, *data):
        msg = []
        msg.append(header)
        msg.extend(data)
        msg.append(hex(self.compute_checksum(map(ord, "".join(msg))))[2:].upper())
        msg.append(self.terminal)
        return ''.join(msg).encode(self.encoding)    

    def parse_response(self, response, header):
        # the last entry is crc
	
        resp = response.decode(self.encoding).split(self.separator)[0:-1]
	#TODO: check whether header == resp[0]
	
        if resp[0] == '$???':
            raise CommunicationError('Device did not understand message')
	

	return resp[1:]
    
    def query(self, transport, header, *data):
        message = self.create_message(header, *data)
        self.logger.debug('Query: %s', repr(message))
        with transport:
            transport.write(message)
            response = transport.read_until(self.terminal.encode(self.encoding))
        self.logger.debug('Response: %s', repr(response))
        return self.parse_response(response,header)

    def write(self, transport, header, *data):
        message = self.create_message(header, *data)
        self.logger.debug('Write: %s', repr(message))
        with transport:
            transport.write(message)
        
