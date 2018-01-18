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
from copy import copy
from pathlib import Path
try: # Python 3
    from configparser import ConfigParser
except ImportError: # Python 2
    from ConfigParser import ConfigParser

# Python 3 standard / Python 2 in pip
from appdirs import AppDirs

__all__ = ['Config']

class Config(object):
    """Hermod configuration handling"""

    # Key files dictionnary
    _keys = dict(
        aes=os.environ.get('HERMOD_AES_KEY', 'aes.key'),
        mac=os.environ.get('HERMOD_MAC_KEY', 'mac.key')
    )

    # Daemon HTTP port
    port = int(os.environ.get('PORT', 38394))

    # Metadata fields names
    fields = dict(
        sender=os.environ.get('HERMOD_FROM', 'from'),
        name=os.environ.get('HERMOD_NAME', 'name'),
        redirect=os.environ.get('HERMOD_REDIRECT', 'url'),
        honeypot=os.environ.get('HERMOD_HONEYPOT', 'hermod')
    )

    # SMTP configuration
    smtp = dict(
        sender=os.environ.get('HERMOD_FROM', 'hermod@localhost'),
        server=os.environ.get('MAILGUN_SMTP_SERVER', 'localhost'),
        port=int(os.environ.get('MAILGUN_SMTP_PORT', 25)),
        login=os.environ.get('MAILGUN_SMTP_LOGIN', ''),
        password=os.environ.get('MAILGUN_SMTP_PASSWORD', '')
        # Avoid passing password in command line variables!
    )

    def __init__(self, filename=None):
        if filename is not None:
            self.load(filename)

    def load_fields(self, conf):
        if conf.has_option('Fields', 'From'):
            self.fields.sender = conf.get('Fields', 'From')
        if conf.has_option('Fields', 'Name'):
            self.fields.name = conf.get('Fields', 'Name')
        if conf.has_option('Fields', 'Redirect'):
            self.fields.redirect = conf.get('Fields', 'Redirect')
        if conf.has_option('Fields', 'Honeypot'):
            self.fields.honeypot = conf.get('Fields', 'Honeypot')

    def load_smtp(self, conf):
        if conf.has_option('SMTP', 'Server'):
            self.smtp.server = conf.get('SMTP', 'Server')
        if conf.has_option('SMTP', 'Port'):
            try:
                self.smtp.port = conf.getint('SMTP', 'Port')
            except AttributeError:
                self.smtp.port = int(conf.get('SMTP', 'Port'))
        if conf.has_option('SMTP', 'Login'):
            self.smtp.login = conf.get('SMTP', 'Login')
        if conf.has_option('SMTP', 'Password'):
            self.smtp.password = conf.get('SMTP', 'Password')

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
            try:
                self.port = conf.getint('Server', 'Port')
            except AttributeError:
                self.port = int(conf.get('Server', 'Port'))

        if conf.has_section('Fields'):
            self.load_fields(conf)

        if conf.has_section('SMTP'):
            self.load_smtp(conf)

    @property
    def _conf_path(self):
        """Return path to search configuration file in"""
        # Remove XDG path as it is a non graphical app
        os.environ['XDG_CONFIG_DIRS'] = '/etc:/usr/local/etc'
        appdirs = AppDirs(__name__, __name__, multipath=True)

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
