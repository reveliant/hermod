<img src="hermod/static/logo.png?raw=true" type="image/png"/>

# Hermód

Hermód adds mail sending capability to your static sites (e.g. "Contact us" forms).

It is privacy-aware, protecting your email address from eavesdropper without any account creation, adopting a stateless design

This project is intended to run on a [Heroku](https://heroku.com/) Python dyno with the [Mailgun](https://elements.heroku.com/addons/mailgun) add-on (both of them are free of charge for the expected limited usage) but can also run with any Python 3 installation (with pip) and a SMTP server.

## Quick setup guide

1. [![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)
2. (Optional) Customize the `HERMOD_ADMIN_EMAIL` variable with administrator email address
3. Go to `/endpoint` on your new Hermód instance and fill the form
4. Look at application logs (or administrator mails if you set the variable):

    ```
    Endpoint generated for contact@example.com from example.com:
    http://your-instance.herokuapp.com/QFnFLdnkPW0=/uc8RDeANub8NoSJfG0mYf3aXlg==/T84ffT6bhuNIag3Pb9rCyrVjKY39Hu5w5i9lu8SgpaQ=
    ```

5. Set the generated endpoint adress as target for your form:

    ```html
    <form
        action="http://your-instance.herokuapp.com/QFnFLdnkPW0=/uc8RDeANub8NoSJfG0mYf3aXlg==/T84ffT6bhuNIag3Pb9rCyrVjKY39Hu5w5i9lu8SgpaQ="
        method="POST">
        <p><input type="email" name="from" placeholder="Your email address"/></p>
        <p><textarea name="message" placehold="Your message"></textarea></p>
        <input type="hidden" name="redirect" value="http://domain.com/gotothispageaftersubmition"/>
        <input type="hidden" name="hermod" value=""/>
        <p><input type="submit" value="Send"></p>
    </form>
    ```

6. You should now be ready to handle requests.

## Complete guide and reference

Hermód reads its configuration from two sources:

* environment variables;
* configuration file, if the `HERMOD_CONFIG` environment variable points to it.

### Configuration variables (config.py)

* Various settings:
    * `HERMOD_USE_ENV`: keys variables contain hex-encoded key values, not key filenames (default False),
    * `HERMOD_ADMIN_EMAIL`: administrator email address (for new endpoint notification in forwarded messages, default None),
    * `HERMOD_NEW_ENDPOINT`: enable `/endpoint` and allow new endpoint generation (default True);
* Cryptographic keys (hexadecimal-encoded strings):
    * `HERMOD_KEYS_AES`: encryption key value or filename,
    * `HERMOD_KEYS_MAC`: authentication key value or filename;
* Form fields names:
    * `HERMOD_FIELDS_NAME`: sender name field,
    * `HERMOD_FIELDS_FROM`: sender email address field,
    * `HERMOD_FIELDS_REDIRECT`: redirection URL field,
    * `HERMOD_FIELDS_HONEYPOT`: honeypot field which must remain blank to not be considered as spam;
* Main [Flask-Mail](https://pythonhosted.org/Flask-Mail/) settings:
    * `MAIL_SERVER`: server address (default 127.0.0.1)
    * `MAIL_PORT`: server port (default 25)
    * `MAIL_USE_TLS`: use StartTLS (default False)
    * `MAIL_USE_SSL`: use SSL / TLS (default False)
    * `MAIL_USERNAME`: username
    * `MAIL_PASSWORD`: password (default None)

On Heroku setup, variables are set on first deploy, but you might want to replace generated keys, or set mail settings to your own SMTP server.

### Configuration file

The configuration file is loaded when the `HERMOD_CONFIG` environment variable is set.
Beware that indicated path is relative to the module subdirectory, i.e. a `hermod.cfg` configuration file alongside this README file shoud be referenced by `HERMOD_CONFIG="../hermod.cfg"`.

The configuration file corresponding to default configuration is provided as reference:

```ini
# Keys are loaded from environment instead of from files
HERMOD_USE_ENV = False

# Key files dictionnary
HERMOD_KEYS_AES = 'aes.key'
HERMOD_KEYS_MAC = 'mac.key'

# Metadata fields names
HERMOD_FIELDS_NAME = 'name'
HERMOD_FIELDS_FROM = 'from'
HERMOD_FIELDS_REDIRECT = 'url'
HERMOD_FIELDS_HONEYPOT = 'hermod'

# Administrator email
HERMOD_ADMIN_EMAIL = None

# Allow new endpoint generation
HERMOD_NEW_ENDPOINT = True
    
# Flask-Mail configuration
MAIL_SERVER = '127.0.0.1'
MAIL_PORT = 25
MAIL_USE_TLS = False
MAIL_USE_SSL = False
MAIL_USERNAME = None
MAIL_PASSWORD = None
```

### Cryptography usage

#### Encryption

* destination email address is encrypted with AES-128 (CTR mode);
* ensure destination address privacy;
* avoid spam from plaintext address in HTML pages.

#### Authentication

* destination email address and redirection URL are sealed with HMAC (SHA-256);
* ensure parameters integrity;
* avoid insecure redirection.

### Endpoint format

Endpoint URL contains cryptographic parameter and messages:
`/<Cipher IV>/<Ciphered destination email address>/<MAC>`

### Command line tools

Generate AES and MAC keys:

   ``` bash
   openssl rand -hex 16 | tee aes.key
   openssl rand -hex 16 | tee mac.key
   chmod go-rwx aes.key mac.key
    ```

## License

This projet is released under GNU General Public License, version 3.
