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

"""Hermod package root"""

import os
from flask import Flask, render_template, request
from .utils import signature, Config, Crypto, aes_iv

__path__ = __import__('pkgutil').extend_path(__path__, __name__)

__all__ = ['APP']

APP = Flask(__name__)
APP.logger.setLevel(0)

config = Config(os.environ.get('HERMOD_CONFIG', None))
# APP.config.<update>(config)

@APP.route('/')
def placeholder():
    return render_template('response.html')

@APP.route('/endpoint', methods=['GET', 'POST'])
def endpoint():
    if request.method == 'POST':
        crypto = Crypto(config.keyfiles)
        cipher_iv = aes_iv()
        ciphertext = crypto.encrypt(cipher_iv, request.form['address'])
        digest = signature(request.form['address'], request.form['redirect'])
        hmac = crypto.sign(digest)

        text = 'Set the Hermod API endpoint to the following value:\n{0}send/{1}/{2}/{3}'
        APP.logger.debug(text.format(request.host_url, cipher_iv, ciphertext, hmac))
        # mail
        return ''
    else:
        return render_template('response.html')

@APP.route('/send/<cipher_iv>/<ciphertext>/<hmac>', methods=['POST'])
def handle(cipher_iv, ciphertext, hmac):
    return '{0}\n{1}\n{2}\n{3}'.format(request.form, cipher_iv, ciphertext, hmac)