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

"""Configuration utilities"""

import os

__all__ = ['Config']

class Config:
    """Hermod default configuration"""

    # Keys are loaded from environment instead of from files
    HERMOD_USE_ENV = os.environ.get('HERMOD_USE_ENV', False)
    
    # Key files dictionnary
    HERMOD_KEYS_AES = os.environ.get('HERMOD_KEYS_AES', 'aes.key')
    HERMOD_KEYS_MAC = os.environ.get('HERMOD_KEYS_MAC', 'mac.key')

    # Metadata fields names
    HERMOD_FIELDS_NAME = os.environ.get('HERMOD_FIELDS_NAME', 'name')
    HERMOD_FIELDS_FROM = os.environ.get('HERMOD_FIELDS_FROM', 'from')
    HERMOD_FIELDS_REDIRECT = os.environ.get('HERMOD_FIELDS_REDIRECT', 'url')
    HERMOD_FIELDS_HONEYPOT = os.environ.get('HERMOD_FIELDS_HONEYPOT', 'hermod')
    
    # Administrator email
    HERMOD_ADMIN_EMAIL = os.environ.get('HERMOD_ADMIN_EMAIL', None)
    
    # Allow new endpoint generation
    HERMOD_NEW_ENDPOINT = os.environ.get('HERMOD_NEW_ENDPOINT', True)
    
    # Flask-Mail configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER', '127.0.0.1')
    MAIL_PORT = os.environ.get('MAIL_PORT', 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', False)
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', False)
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', None)
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', None)