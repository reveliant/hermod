# Hermod

Hermod adds mail sending capability to your static sites (e.g. "Contact us" forms).

It's privacy-aware, protecting your email address from eavesdropper without any account creation.

No database nor further server configuration is required after setting some variables.

To configure new forms, you'll just need to set the action URL with a token computed with provided utility and *voila*!

## Setup guide

This project is intended to run on a [Heroku](https://heroku.com/) Python dyno with the [Mailgun](https://elements.heroku.com/addons/mailgun) add-on (both of them are free of charge for the expected limited usage). You can also run it standalone with Python 3 and a SMTP server.

### Prerequisite

Create an AES-128 key (and keep it secret!):
```Shell
$ openssl rand -base64 16 > hermod.key
$ chmod go-rwx hermod.key
```

That key will be used:
 * to encrypt destination email address, avoiding eavesdropper and spam;
 * to sign (HMAC) critical fields, avoiding insecure redirection after submission.

### Heroku setup

1. [![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)
2. Set `HERMOD_KEY` config variable with the previously generated AES key (base64 string)
  
### On promise setup

1. Install Python 3 + pip
2. Clone repository
3. Install dependancies:
```Shell
$ pip install -r requirements.txt
```
4. Set environment variables:
  * `HERMOD_KEY` with the previously generated AES key,
  * `MAILGUN_SMTP_LOGIN`, `MAILGUN_SMTP_PASSWORD`, `MAILGUN_SMTP_SERVER` and `MAILGUN_SMTP_PORT` with appropriate parameters for your SMTP server,
  * Note that `MAILGUN` is kept on variables names to speed up setting of Heroku instance; you don't actually need to use Mailgun services at all.
5. Start server:
```Shell
$ python hermod-daemon.py PORT
```

### Setup new form

1. If you haven't already, copy `hermod.py` localy and make it executable

2. Compute endpoint token with `hermod.py` utility :
  * previously generated AES key (`-k|--key`)
  * destination email address (`-m|--mail`)
  * URL to redirect to after submission (`-r|--redirect`):
  
  e.g.:
```Shell
$ ./hermod.py -k hermod.key -m contact-me@domain.com -r http://domain.com/gotothispageaftersubmition
Set the API endpoint to the following value:
<api root>/rax6y9io-dV9-OD_g9sB22e7/e259e919c742fb6381925c148cb1cacc665f5f7626645fde003c98b79c315fe8
```

3. Set the target URL on your form to point your instance with the token, and set the "redirect" field, e.g.:
```HTML
<form
      action="http://your-instance.herokuapp.com/send/rax6y9io-dV9-OD_g9sB22e7/e259e919c742fb6381925c148cb1cacc665f5f7626645fde003c98b79c315fe8"
      method="POST">
    <p><input type="email" name="from" placeholder="Your email address"/></p>
    <p><textarea name="message" placehold="Your message"></textarea></p>
    <input type="hidden" name="redirect" value="http://domain.com/gotothispageaftersubmition"/>
    <p><input type="submit" value="Send"></p>
</form>
```

## License

This projet is released under GNU General Public License, version 3.