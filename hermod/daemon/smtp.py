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

import errno
from smtplib import SMTP, SMTPException
try: #Python 3
    from email.message import EmailMessage
except ImportError: # Python 2
    from email.message import Message as EmailMessage

__all__ = ['MailClient', 'MailError']

class MailError(Exception):
    """This exception is raised when something is wrong with SMTP"""
    pass

class MailClient(object):
    """Mail client class"""
    def __init__(self, config):
        self._msg = None
        self._from = config.smtp.sender

        try:
            self._smtp = SMTP(config.smtp.server, config.smtp.port)
            self._smtp.starttls()
            if config.smtp.login != '':
                self._smtp.login(config.smtp.login, config.smtp.password)
        except SMTPException as err:
            raise MailError('Undefined SMTP error')
        except OSError as err:
            if err.errno == errno.ECONNREFUSED:
                raise MailError('Unable to connect to {0}:{1}'.format(config.smtp.server, config.smtp.port))
            else:
                raise MailError('Undefined OS error while sending mail')

    def send(self, addr, message=None):
        """Send messagg to addr"""
        msg = EmailMessage()

        msg.add_header('Subject', 'Message via Hermod')
        msg.add_header('From', self._from)
        msg.add_header('To', addr)

        if isinstance(message, dict):
            body = ''
            for key in message:
                body += '{0}:\r\n{1}\r\n\r\n'.format(key, message[key])
            msg.set_content(body)
        else:
            msg.set_content(str(message))

        try:
            self._smtp.send_message(msg)
        finally:
            self._smtp.quit()
