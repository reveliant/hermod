#!/usr/bin/env python
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

"""Hermod daemon starter"""

from __future__ import (absolute_import, division, print_function)

from argparse import ArgumentParser

from hermod.daemon.http import HTTPServer
from hermod.utils import signature
from hermod.utils.config import Config
from hermod.utils.crypto import Crypto, aes_iv

class Hermod(object):
    """Hermod program"""
    def __init__(self):
        self.parse_args()

        if self.args.use_env:
            self.args.filename = None
        self.config = Config(self.args.filename)

        if self.args.as_daemon:
            if self.args.daemon_port is not None:
                self.config.port = self.args.daemon_port
            self.daemon()
        else:
            self.client()

    def parse_args(self):
        """Load config from command-line arguments"""
        parser = ArgumentParser(
            description='Give the Hermod API endpoint for the following options',
            epilog='Daemon mode and command line mode options are incompatible'
        )

        config = parser.add_argument_group('Configuration options')
        config.add_argument('-c', '--config', default='hermod.cfg', dest='filename',
                            metavar='FILE', help='Custom configuration file')
        config.add_argument('-e', '--env', dest='use_env', action='store_true',
                            help='Use only environment vars')

        daemon = parser.add_argument_group('Daemon mode options')
        daemon.add_argument('-d', '--daemon', dest='as_daemon', action='store_true',
                            help='Start as daemon')
        daemon.add_argument('-p', '--port', dest='daemon_port', nargs='?', type=int,
                            metavar='PORT', help='Listen on port PORT')

        cli = parser.add_argument_group('Command line mode options')
        cli.add_argument('address', nargs='?',
                         metavar='EMAIL', help='Payload will be sent to this email address')
        cli.add_argument('redirect', nargs='?',
                         metavar='URL', help='User will be redirect to that URL after submission')

        self.args = parser.parse_args()

        if self.args.as_daemon:
            if self.args.address or self.args.redirect:
                raise parser.error('Daemon mode and command line mode options are incompatible')
        else:
            if not self.args.address or not self.args.redirect:
                raise parser.error('EMAIL and URL are required in command line mode')

    def daemon(self):
        """Start HTTP daemon"""
        server = HTTPServer(self.config)
        try:
            server.start()
        except KeyboardInterrupt:
            print('Interruption received, shutting down server')
            server.stop()

    def client(self):
        """Generate crypto elements for API"""
        crypto = Crypto(self.config.keyfiles)
        cipher_iv = aes_iv()
        ciphertext = crypto.encrypt(cipher_iv, self.args.address)
        digest = signature(self.args.address, self.args.redirect)
        hmac = crypto.sign(digest)

        text = 'Set the Hermod API endpoint to the following value: /%s/%s/%s'
        print(text % (cipher_iv, ciphertext, hmac))


if __name__ == '__main__':
    Hermod()
