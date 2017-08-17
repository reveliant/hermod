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
from email.message import EmailMessage

__all__ = ['MailClient']

class MailClient(object):
    """Mail client class"""
    def __init__(self, config):
        self._msg = None
        self._from = config.smtp.sender
        self._smtp = SMTP(config.smtp.server, config.smtp.port)
        self._smtp.starttls()
        if config.smtp.login != '':
            self._smtp.login(config.smtp.login, config.smtp.password)

    def send(self, addr, message=None):
        """Send messagg to addr"""
        msg = EmailMessage()
        
        msg['Subject'] = 'Message via Hermod'
        msg['From'] = self._from
        msg['To'] = addr
                    
        if isinstance(message, dict):
          body = ''
          for key in message:
            body += '%s:\r\n%s\r\n\r\n' % (key, message[key])
          msg.set_content(body)
        else:
          msg.set_content(str(message))
          
        try:
          self._smtp.send_message(msg)
        finally:
          self._smtp.quit()
