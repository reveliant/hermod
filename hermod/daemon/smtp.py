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

"""Mail features fro Hermod"""

from __future__ import (absolute_import, division, print_function)

from smtplib import SMTP

__all__ = ['MailClient']

class MailClient(object):
    """Mail client class"""
    def __init__(self, config):
        self._msg = None
        self._smtp = SMTP(config.smtp.server, config.smtp.port)
        self._smtp.connect()
        self._smtp.starttls()
        if config.smtp.login != '':
            self._smtp.login(config.smtp.login, config.smtp.password)

    def send(self, addr, msg=None):
        """Send msg to addr"""
        if msg is None:
            msg = self._msg

        self._smtp.sendmail(
            'hermod@instance.org',
            addr,
            msg
            )
        self._smtp.quit()
