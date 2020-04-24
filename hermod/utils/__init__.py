# coding=utf-8
# (c) 2017, Rémi Dubois <packman@oxiame.net>
#
# This file is part of Hermód
#
# Hermód is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hermód is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Hermod.  If not, see <http://www.gnu.org/licenses/>.

"""Hermod various utilities"""

try: # Python 3
  from urllib.parse import urlparse
except ImportError: # Python 2
  from urlparse import urlparse

from .config import Config
from .crypto import Crypto

__all__ = ['signature', 'urlparse', 'Config', 'Crypto']

def signature(address=None, domain=None):
    """Signature string to compute digest from"""
    return '{0}\n{1}'.format(address, domain)
