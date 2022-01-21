Configuration
=============

Hermód reads its configuration from two sources:

-   environment variables;
-   configuration file, if the ``HERMOD_CONFIG`` environment variable points to it.


Configuration variables (in config.py)
--------------------------------------

-   Various settings:

    .. py:data:: HERMOD_USE_ENV

        keys variables contain hex-encoded key values, not key filenames (default ``False``)

    .. py:data:: HERMOD_ADMIN_EMAIL

        administrator email address (for new endpoint notification in forwarded messages, default ``None``)

    .. py:data:: HERMOD_NEW_ENDPOINT

        enable ``/endpoint`` and allow new endpoint generation (default ``True``)

-   Cryptographic keys (hexadecimal-encoded strings):

    .. py:data:: HERMOD_KEYS_AES
  
        encryption key value or filename
    
    .. py:data:: HERMOD_KEYS_MAC
    
        authentication key value or filename
    
-   Form fields names:

    .. py:data:: HERMOD_FIELDS_NAME

        sender name field

    .. py:data:: HERMOD_FIELDS_FROM

        sender email address field

    .. py:data:: HERMOD_FIELDS_REDIRECT

        redirection URL field

    .. py:data:: HERMOD_FIELDS_HONEYPOT

        honeypot field which must remain blank to not be considered as spam

-   Main `Flask-Mail`_ settings:

    .. py:data:: MAIL_SERVER

        server address (default ``127.0.0.1``)

    .. py:data:: MAIL_PORT

        server port (default ``25``)

    .. py:data:: MAIL_USE_TLS

        use StartTLS (default ``False``)

    .. py:data:: MAIL_USE_SSL

        use SSL / TLS (default ``False``)

    .. py:data:: MAIL_USERNAME

        username

    .. py:data:: MAIL_PASSWORD

        password (default ``None``)

    .. py:data:: MAIL_DEFAULT_SENDER

        email From field (default ``"Hermód <`MAIL_UNSERNAME`>"``)

.. _Flask-Mail: https://pythonhosted.org/Flask-Mail/

On Heroku setup, variables are set on first deploy, but you might want to replace generated keys, or set mail settings to your own SMTP server.

Configuration file
------------------

The configuration file is loaded when the ``HERMOD_CONFIG`` environment variable is set.
Beware that indicated path is relative to the module subdirectory, i.e. a ``hermod.cfg`` configuration file alongside this README file shoud be referenced by ``HERMOD_CONFIG="../hermod.cfg"``.

The configuration file corresponding to default configuration is provided as reference::

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
