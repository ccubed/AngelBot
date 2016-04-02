Security and Oauth
==================

AngelBot can obtain Oauth for some APIs (And for others it's necessary because no public access exists). This can be scary and many people will worry about security. This document discusses what is being done to protect your information.

Storage
-------

Everything is stored locally on a server behind two stateful firewalls on an up to date Apache and Linux setup.
The database is redis. This server has an SSL Certificate. You can visit the angelbot website through https://angelbot.vertinext.com .

Security
--------

The Oauth section of the server runs on a flask setup with SSL Credentials. You'll see the lock next to your address bar.

The server only accepts TLS connections encrypted with AES. It won't accept lesser encryption protocols. Attempting to visit the site with an out of date browser will simply yield an error.

Keys are encrypted using a 256 random bytes from urandom and AES.