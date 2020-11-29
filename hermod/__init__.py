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

"""Hermod package root"""

import os
from pprint import pprint
from flask import Flask, render_template, request, redirect
from flask_mail import Mail, Message
from .utils import signature, urlparse, Config, Crypto

__path__ = __import__('pkgutil').extend_path(__path__, __name__)

__all__ = ['app']

app = Flask(__name__)

app.config.from_object(Config)
if 'HERMOD_CONFIG' in os.environ:
  app.config.from_envvar('HERMOD_CONFIG')
app.config['MAIL_DEFAULT_SENDER'] = 'Hermód <{0}>'.format(app.config.get('MAIL_USERNAME'))

mail = Mail(app)
crypto = Crypto(app.config.get_namespace('HERMOD_KEYS_'), app.config.get('HERMOD_USE_ENV'))

@app.route('/')
def placeholder():
    return render_template('response.html', page='hello')
  
@app.route('/endpoint')
def endpoint_form():
    if app.config.get('HERMOD_NEW_ENDPOINT'):
        return render_template('response.html', page='endpoint')
    else:
        return render_template('response.html', error='Endpoint generation has been disabled by administrator'), 403
  
@app.route('/endpoint', methods=['POST'])
def endpoint_action():
    if app.config.get('HERMOD_NEW_ENDPOINT'):
          endpoint = {
            'address': request.form['address'],
            'redirect': request.form['redirect'],
            'domain': urlparse(request.form['redirect']).netloc,
            'fields': app.config.get_namespace('HERMOD_FIELDS_')
          }

          cipher_iv = crypto.aes_iv()
          ciphertext = crypto.encrypt(cipher_iv, endpoint['address'])

          digest = signature(endpoint['address'], endpoint['domain'])
          hmac = crypto.sign(digest)

          endpoint['url'] = '{0}send/{1}/{2}/{3}'.format(request.host_url, cipher_iv, ciphertext, hmac)

          text = 'Endpoint generated for {address} from {domain}:\n{url}'.format_map(endpoint)
          app.logger.info(text)

          if app.config.get('HERMOD_ADMIN_EMAIL') not in [None, '']:
                msg = Message('Your new Hermód endpoint')
                msg.add_recipient(app.config.get('HERMOD_ADMIN_EMAIL'))
                msg.html = render_template('mail.html', endpoint=endpoint)
                mail.send(msg)

          return render_template('response.html', page="endpoint-success")
    else:
          return render_template('response.html', error='Endpoint generation has been disabled by administrator'), 403

@app.route('/send/')
def send_form():
    return render_template('response.html', page='send', fields=app.config.get_namespace('HERMOD_FIELDS_'))

@app.route('/send/<cipher_iv>/<ciphertext>/<hmac>', methods=['POST'])
def send_action(cipher_iv, ciphertext, hmac):
    fields = app.config.get_namespace('HERMOD_FIELDS_')
    form = request.form.copy()
    
    address = crypto.decrypt(cipher_iv, ciphertext)
    redirect_to = form.pop(fields.get('redirect'), default=request.referrer)

    honeypot = form.pop(fields.get('honeypot'), default=None)
    if honeypot != '':
        return render_template('response.html', error='Content tampered'), 403
    
    domain = urlparse(redirect_to).netloc
    if domain is None:
        domain = urlparse(request.referrer).netloc
    digest = signature(address, domain)
    if not crypto.verify(digest, hmac):
        return render_template('response.html', error='Content tampered'), 403
    
    message = {
        'origin': request.referrer,
        'sender': form.pop(fields.get('name'), default=None),
        'address': form.pop(fields.get('from'), default=None),
        'administrator': app.config.get('HERMOD_ADMIN_EMAIL'),
        'fields': form
    }

    text = 'Received message from {m.sender} <{m.address}> for {a} via {m.origin}'.format_map(m=message, a=address)
    app.logger.info(text)
    
    if message['address'] is None:
        return render_template('response.html', error='A required field is missing: your email address'), 400
    
    msg = Message('New  message via Hermód')
    msg.add_recipient(address)
    if message['sender'] is not None:
        msg.reply_to = (message['sender'], message['address'])
    else :
        msg.reply_to = message['address']
    msg.html = render_template('mail.html', message=message)
    mail.send(msg)
    
    return redirect(redirect_to)