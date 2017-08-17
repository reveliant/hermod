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

"""Configuration utilities"""

from __future__ import (absolute_import, division, print_function)

import os
import sys
try: # Python 3
    from configparser import ConfigParser
except ImportError: # Python 3
    from ConfigParser import ConfigParser
from copy import copy
from pathlib import Path

from appdirs import AppDirs

from hermod.utils import APPNAME, Attributes

__all__ = ['Config']

class Config(object):
    """Hermod configuration handling"""

    # Key files dictionnary
    _keys = Attributes(
        aes=os.environ.get('HERMOD_AES_KEY', 'aes.key'),
        mac=os.environ.get('HERMOD_MAC_KEY', 'mac.key')
        )

    # Daemon HTTP port
    port = int(os.environ.get('PORT', 38394))

    # Metadata fields names
    fields = Attributes(
        redirect=os.environ.get('HERMOD_REDIRECT', 'url'),
        honeypot=os.environ.get('HERMOD_HONEYPOT', 'hermod')
        )

    # SMTP configuration
    smtp = Attributes(
        sender=os.environ.get('HERMOD_FROM', 'hermod@localhost'),
        server=os.environ.get('MAILGUN_SMTP_SERVER', 'localhost'),
        port=int(os.environ.get('MAILGUN_SMTP_PORT', 25)),
        login=os.environ.get('MAILGUN_SMTP_LOGIN', ''),
        password=os.environ.get('MAILGUN_SMTP_PASSWORD', '')
        # Avoid passing password in command line variables!
        )

    def __init__(self, filename):
        if filename is not None:
            self.load(filename)

    def load(self, filename):
        """Load configuration file"""
        if not Path(filename).is_absolute():
            filename = [str(Path(directory).joinpath(filename)) for directory in self._conf_path]

        conf = ConfigParser()
        conf.read(filename)

        if conf.has_section('Keys'):
            for cfg in conf.items('Keys'):
                self._keys[cfg[0]] = self._find_keyfile(cfg[1])

        if conf.has_option('Server', 'Port'):
            self.port = conf.get_int('Server', 'Port')

        if conf.has_option('Fields', 'Redirect'):
            self.fields.redirect = conf.get('Fields', 'Redirect')
        if conf.has_option('Fields', 'Honeypot'):
            self.fields.honeypot = conf.get('Fields', 'Honeypot')

        if conf.has_option('SMTP', 'Server'):
            self.smtp.server = conf.get('SMTP', 'Server')
        if conf.has_option('SMTP', 'Port'):
            self.smtp.port = conf.get_int('SMTP', 'Port')
        if conf.has_option('SMTP', 'Login'):
            self.smtp.login = conf.get('SMTP', 'Login')
        if conf.has_option('SMTP', 'Password'):
            self.smtp.password = conf.get('SMTP', 'Password')

    @property
    def _conf_path(self):
        # Remove XDG path as it is a non graphical app
        os.environ['XDG_CONFIG_DIRS'] = '/etc:/usr/local/etc'
        appdirs = AppDirs(APPNAME, APPNAME, multipath=True)

        confpath = appdirs.site_config_dir.split(os.pathsep)
        confpath.append(appdirs.user_config_dir)
        confpath.append(os.getcwd())

        return confpath

    def _find_keyfile(self, filename):
        """Return absolute path for a key file"""
        confpath = list(self._conf_path)
        confpath.reverse()
        for path in confpath:
            keyfile = Path(Path(path).joinpath(filename))
            if keyfile.is_file():
                return keyfile.open('rb')
        print('Unable to find key \'%s\' in %s' % (filename, confpath), file=sys.stderr)
        return None

    @property
    def keyfiles(self):
        """Return key files list"""
        return copy(self._keys)
