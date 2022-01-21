.. rst-class:: hide-header

Welcome to Hermod
=================

.. image:: https://github.com/reveliant/hermod/raw/master/hermod/static/logo.png?raw=true
    :alt: Hermód: mail for you static site
    :align: center

**Hermód** adds mail sending capability to your static sites (e.g. "Contact us" forms).

It is privacy-aware, protecting your email address from eavesdropper without any account creation, adopting a stateless design

This project is intended to run on a `Heroku`_ Python dyno with the `Mailgun`_ add-on (both of them are free of charge for the expected limited usage) but can also run with any Python 3 installation (with pip) and a SMTP server.

.. _Heroku: https://heroku.com
.. _Mailgun: https://elements.heroku.com/addons/mailgun

User's Guide
------------

.. toctree::

   quickstart
   configuration
   cryptography

License
-------

This projet is released under GNU General Public License, version 3.
