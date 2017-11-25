<img src="logo.png?raw=true" type="image/png"/>

# Hermód

Hermód adds mail sending capability to your static sites (e.g. "Contact us" forms).

It is privacy-aware, protecting your email address from eavesdropper without any account creation.

This project is intended to run on a [Heroku](https://heroku.com/) Python dyno with the [Mailgun](https://elements.heroku.com/addons/mailgun) add-on (both of them are free of charge for the expected limited usage) but can also run with any Python 2 or 3 installation (with pip) and a SMTP server.

## Quick setup guide

1. Clone repository on your computer and install Python dependancies:

   ``` bash
   pip install -r requirements.txt
   ```
   
2. Generate AES and MAC keys:

   ``` bash
   openssl rand -base64 16 | tee aes.key
   openssl rand -base64 16 | tee mac.key
   chmod go-rwx aes.key mac.key
    ```

3. [![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)
4. On Heroku, customize `HERMOD_*` variables (at least `HERMOD_AES_KEY` and `HERMOD_MAC_KEY`).

You are now ready to handle requests.

### Setting up a new form

On your computer, generate a token for new form:

```bash
python hermod.py 'contact@example.com' 'http://example.com/gotothispageaftersubmition'
Set the Hermod API endpoint to the following value:
/QFnFLdnkPW0=/uc8RDeANub8NoSJfG0mYf3aXlg==/T84ffT6bhuNIag3Pb9rCyrVjKY39Hu5w5i9lu8SgpaQ=
```

You can now fill your HTML form:

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

## Complete guide and reference

Hermód reads its configuration from two sources (the later taking precedence):

* environment variables;
* configuration file.

### Environment variables

* Cryptographic keys (base64-encoded strings):
    * `HERMOD_AES_KEY`: for encryption,
    * `HERMOD_MAC_KEY`: for signature;
* Server:
    * `PORT`: HTTP server port number
* Form fields names:
    * `HERMOD_REDIRECT`: name of redirection URL field,
    * `HERMOD_HONEYPOT`: name of honeypot field which must remain blank to avoid spam;
* SMTP settings:
    * `HERMOD_FROM`: 'From' address. No reply is expected from such address.
    * `MAILGUN_SMTP_SERVER`: server name
    * `MAILGUN_SMTP_PORT`: server port
    * `MAILGUN_SMTP_LOGIN`: login
    * `MAILGUN_SMTP_PASSWORD`: password
    * You are not tied to Mailgun service: those variables names are use to speed up Heroku configuration.

On Heroku setup, only `HERMOD_*` variables have to be set.

### Configuration file

The configuration file is expected to be on the current directory, on user configuration directory or on system-wide configuration directory (e.g. `~/.config/hermod/` and `/etc/hermod/` on Linux for the latest).
Default filename is `hermod.cfg`.

Here is an sample config file for reference. Each section and parameter are optional, and defaults values are show.

```ini
[Keys]
AES = aes.key
MAC = hmac.key

[Server]
Port = 38394

[Fields]
From = from
Name = name
Redirect = url
Honeypot = hermod

[SMTP]
From = hermod@localhost
Server = localhost
Port = 25
Login = 
Password = 
```

### Cryptography usage

#### Encryption

* destination email address is encrypted with AES-128 (CTR mode);
* ensure destination address privacy;
* avoid spam from plaintext address in HTML pages.

#### Signature

* email address and redirection URL are signed with HMAC (SHA-256);
* ensure parameters integrity;
* avoid insecure redirection.

### Command line options

    hermod.py [-he] [-c FILE] {EMAIL ADDRESS} {REDIRECT_URL}
    hermod.py [-he] [-c FILE] -d [-p PORT]

#### General options

* `-h|--help` : show help message
* `-e|--env`: use only environment variables and no configuration file
* `-c|--conf FILE`: use FILE instead of default configuration file name and path

#### Token generation options

* `EMAIL ADDRESS`: messages will be send to this address
* `REDIRECT_URL`: client will be redirected to that URL after submission

#### Server options

* `-d|--daemon`: start as daemon and do not compute token
* `-p|--port PORT`: listen on port PORT

## License

This projet is released under GNU General Public License, version 3.