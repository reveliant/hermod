#!/usr/bin/env python
"""
Hermod command line utility
Copyright (C) 2017  Rémi Dubois

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import sys
import argparse
from base64 import b64decode, urlsafe_b64encode, urlsafe_b64decode
import yaml
from Crypto.Cipher import AES
from Crypto.Util import Counter
from Crypto import Random
from Crypto.Hash import HMAC, SHA256

class SignConfig(object):
    """
    Configuration class for StaticMail
    """
    key = None
    __key = None
    address = None
    url = None

    def __init__(self):
        pass

    def from_args(self):
        """
        Load config from command-line arguments
        """
        parser = argparse.ArgumentParser(
            description='Give RSA signature for the following options',
            epilog='Program will read for YAML on standard input if no argument is given'
        )
        parser.add_argument('-k', '--key', dest='key', help='AES key file')
        parser.add_argument('-m', '--mail', dest='address', help='send email to ADDRESS')
        parser.add_argument('-r', '--redirect', dest='url', help='redirect to URL on success')
        parser.parse_args(namespace=self)

    def from_yaml(self, file):
        """
        Load config from standard input YAML content
        """
        raw_yaml = yaml.safe_load(file)

        if raw_yaml is None:
            print('No config available on standard input')
            exit()
        else:
            self.__dict__ = raw_yaml

    def check(self):
        """
        Check object properties
        """
        check = True

        if self.key is None:
            print('Missing AES key file')
            check = False
        else:
            with open(self.key, mode='rb') as keyfile:
                self.__aes_key = b64decode(keyfile.read(24))
                keyfile.read(2) # Consume \r\n
                self.__hmac_key = b64decode(keyfile.read(24))

        if self.address is None:
            print('Missing mail address')
            check = False

        if self.url is None:
            print('Missing redirect URL')
            check = False

        return check
    
    def create_iv(self):
        """
        Generate cryptographic secure pseudo-random number (CSPRN) for initialisation verctor
        """
        iv = Random.get_random_bytes(8)
        return urlsafe_b64encode(iv).decode('utf-8')

    def encrypt(self, iv):
        """
        Encrypt email address with AES key
        """
        message = self.address.encode('ascii')
        ctr = Counter.new(64, prefix=urlsafe_b64decode(iv))
        cipher = AES.new(self.__aes_key, AES.MODE_CTR, counter=ctr)
        ciphertext = cipher.encrypt(message)
        return urlsafe_b64encode(ciphertext).decode('utf-8')

    def sign(self):
        """
        Sign email address and redirect-URL with key
        """
        message = ('address:%s\nredirect:%s' % (self.address, self.url)).encode('ascii')
        hmac = HMAC.new(self.__hmac_key, msg=message, digestmod=SHA256)
        return urlsafe_b64encode(hmac.digest()).decode('utf-8')

def main():
    """
    Main program
    """
    config = SignConfig()

    if len(sys.argv) > 1:
        # Arguments where given to script
        config.from_args()
    else:
        # No argument was given: read YAML from standard input
        config.from_yaml(sys.stdin)

    if config.check():
        iv = config.create_iv()
        ciphertext = config.encrypt(iv)
        hmac = config.sign()
        text = 'Set the API endpoint to the following value:\n\n<api root>/%s/%s/%s\n'
        print(text % (iv, ciphertext, hmac))

if __name__ == '__main__':
    main()
