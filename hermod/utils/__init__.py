# coding=utf-8
# (c) 2017, Rémi Dubois <packman@oxiame.net>
#
# This file is part of Hermod
#
# Hermod is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hermod is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Hermod.  If not, see <http://www.gnu.org/licenses/>.

"""Hermod various utilities"""

from __future__ import (absolute_import, division, print_function)

__all__ = ['APPNAME', 'Attributes', 'signature']

APPNAME = 'hermod'

class Attributes(dict):
    """SimpleNamespace alternative"""
    def __getattr__(self, attr):
        return self[attr]

    def __setattr__(self, attr, value):
        self[attr] = value

    def __delattr__(self, attr):
        del self[attr]

    def __copy__(self):
        return type(self)(self)

def signature(address=None, url=None):
    """Signature string to compute digest from"""
    return 'address: {0}\nredirect: {1}'.format(address, url)
