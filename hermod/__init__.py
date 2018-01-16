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

from flask import Flask, render_template

__path__ = __import__('pkgutil').extend_path(__path__, __name__)

app = Flask(__name__)

@app.route('/')
def placeholder():
    return render_template('response.html')

@app.route('/new')
def show_new_form():
    return render_template('response.html')

@app.route('/endpoint', method=['POST'])
def register_endpoint():
    return None

@app.route('/send/<iv>/<ciphered>/<hmac>', method=['POST'])
def send_form(iv, ciphered, hmac):
    return None