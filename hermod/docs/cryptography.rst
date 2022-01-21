Cryptography usage
==================

Encryption
----------

-   destination email address is encrypted with AES-128 (CTR mode);
-   ensure destination address privacy;
-   avoid spam from plaintext address in HTML pages.

Authentication
--------------

-   destination email address and redirection domain name are sealed with HMAC (SHA-256);
-   ensure parameters integrity;
-   avoid insecure redirection.

Note that if a redirection URL is not provided (no ``HERMOD_FIELDS_REDIRECT`` field), referrer will be use and its domain checked againts insecure redirection.

Endpoint format
---------------

Endpoint URL contains cryptographic parameter and messages:
``/<Cipher IV>/<Ciphered destination email address>/<MAC>``