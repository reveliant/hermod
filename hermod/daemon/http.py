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

"""HTTP server and requests handler"""

from __future__ import (absolute_import, division, print_function)

import os
import sys
try: # Python 3
    from http.server import HTTPServer as PyHTTPServer, BaseHTTPRequestHandler
except ImportError: # Python 2
    from BaseHTTPServer import HTTPServer as PyHTTPServer, BaseHTTPRequestHandler
import mimetypes
from cgi import FieldStorage
from binascii import Error as PaddingError
import shutil
from pathlib import Path
from pkg_resources import resource_filename

from hermod.daemon.smtp import MailClient
from hermod.utils import APPNAME, Attributes, signature
from hermod.utils.crypto import Crypto

__all__ = ['HTTPServer']

class HTTPServer(PyHTTPServer):
    """HTTP server daemon"""
    def __init__(self, config):
        server_address = ('', config.port)
        PyHTTPServer.__init__(self, server_address, RequestHandler)
        self.config = config
        self.crypto = Crypto(config.keyfiles)

    def start(self):
        """Start daemon"""
        print('Hermod listening on port: %i' % self.config.port)
        self.serve_forever()

    def stop(self):
        """Stop daemon"""
        self.socket.close()

class MalformedError(Exception):
    """This exception is raised when some data is missing or cannot be read"""
    pass

class TamperedError(Exception):
    """This exception is raised when data has been tampered"""
    pass

class RequestHandler(BaseHTTPRequestHandler):
    """Request handler for Hermod API"""
    server_version = 'Hermod'
    sys_version = ''
    close_connection = True

    config = None
    crypto = None

    fields = dict()

    metadata = Attributes(
        address=None,
        redirect=None,
        digest=None
        )

    if not mimetypes.inited:
        mimetypes.init() # try to read system mime.types

    extensions_map = mimetypes.types_map.copy()
    extensions_map.update({
        '': 'application/octet-stream', # Default
        '.py': 'text/plain',
        '.c': 'text/plain',
        '.h': 'text/plain',
        })

    def do_HEAD(self): # pylint: disable=invalid-name
        """Handle HEAD method requests"""
        self.send_response(200)
        self.end_headers()

    def do_GET(self): # pylint: disable=invalid-name
        """Handle GET method requests"""
        if self.path != '/':
            self.redirect('/')
        else:
            self.send_file('response.html')

    def do_POST(self): # pylint: disable=invalid-name
        """Handle POST method requests"""
        self.config = self.server.config
        self.crypto = self.server.crypto

        try:
            self.parse_url()
            self.parse_body()
            self.validate_payload()

            mail = MailClient(self.config)
            #sent = mail.send(self.metadata.address, self.fields)
            #if sent:
            self.redirect(self.metadata.redirect)
        except MalformedError as err:
            print(err, file=sys.stderr)
            self.send_error(400, 'Bad request')
        except TamperedError as err:
            print(err, file=sys.stderr)
            self.send_error(403, 'Forbidden')
        except BaseException as err: # Any other exception
            print(err, file=sys.stderr)
            self.send_error(500, 'Internal Server Error')

    def parse_url(self):
        """Extract metadata from URL"""
        try:
            (_, cipher_iv, ciphertext, digest) = self.path.split('/')
        except ValueError:
            raise MalformedError('Wrongly sized URL')

        try:
            self.metadata.address = self.crypto.decrypt(cipher_iv, ciphertext)
            self.metadata.digest = digest
        except PaddingError:
            raise MalformedError('Broken base64 encoding')
        except ValueError:
            raise TamperedError('Tampered IV or ciphertext')

    def parse_body(self):
        """Extract fields and metadata from POST body"""
        body = FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST'},
            keep_blank_values=True
            )

        self.fields = dict()
        for key in body.keys():
            self.fields[key] = body.getvalue(key)

        try:
            # Check honeypot field
            if self.fields[self.config.fields.honeypot] != '':
                raise TamperedError('Honeypot field not empty')
            # Save redirect URL
            self.metadata.redirect = self.fields[self.config.fields.redirect]
        except KeyError as err:
            raise MalformedError('Missing required field: %s' % err.args[0])

        # Remove metadata fields
        del self.fields[self.config.fields.honeypot]
        del self.fields[self.config.fields.redirect]

    def validate_payload(self):
        """Validate signature against URL and fields"""
        digest = signature(self.metadata.address, self.metadata.redirect)
        verified = self.crypto.verify(digest, self.metadata.digest)
        if not verified:
            raise TamperedError('Signature verification failed')

    def send(self, body):
        """Send plain content to client"""
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain;charset=UTF-8')
        self.end_headers()
        self.wfile.write(body)
        self.wfile.write(b'\r\n')

    def send_file(self, filename, headers=None):
        """Send file content to client
        Additionnal headers can be passed as dict"""
        fres = None

        # Guessing Content-Type
        ext = Path(filename).suffix
        if ext in self.extensions_map:
            ctype = self.extensions_map[ext]
        elif ext.lower() in  self.extensions_map:
            ctype = self.extensions_map[ext.lower()]
        else:
            ctype = self.extensions_map['']

        # Opening file
        try:
            if not Path(filename).is_file():
                filename = resource_filename('hermod.resources', filename)
            fres = open(filename, 'rb')
            fstats = os.fstat(fres.fileno())

            self.send_response(200)
            self.send_header("Content-type", ctype)
            self.send_header("Content-Length", str(fstats[6]))
            self.send_header("Last-Modified", self.date_time_string(fstats.st_mtime))

            if isinstance(headers, dict):
                for name in headers:
                    self.send_header(name, headers[name])
            self.end_headers()

            shutil.copyfileobj(fres, self.wfile)
            fres.close()
        except OSError:
            self.send_error(404, 'File not found')

    def redirect(self, location):
        """Send temporary redirection to client"""
        self.send_response(302)
        self.send_header('Location', location)
        self.end_headers()
