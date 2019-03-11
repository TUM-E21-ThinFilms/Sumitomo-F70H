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

from sumitomo_f70h.protocol import SumitomoF70HProtocol

from sumitomo_f70h.driver import SumitomoF70HDriver

from e21_util.transport import Serial
from e21_util.log import get_sputter_logger
from e21_util.ports import Ports

class SumitomoF70HFactory(object):

	@staticmethod
	def create(transport, logger):
		return SumitomoF70HDriver(SumitomoF70HProtocol(transport, logger))


	def get_logger(self):

		return get_sputter_logger('Sumitomo F-70H', 'sumitomo.log')
	
	def create(self, device=None, logger=None):
		if logger is None:
			logger = self.get_logger()

		if device is None:
			device = Ports().get_port(Ports.DEVICE_COMPRESSOR)

		protocol = SumitomoF70HProtocol(logger=logger)
		return SumitomoF70HDriver(Serial(device, 9600, 8, 'N', 1, 1), protocol)
