.. AngelBot documentation master file, created by
   sphinx-quickstart on Mon Apr  4 20:25:30 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to AngelBot's documentation!
====================================

Contents:

.. toctree::
   XIVDB
   Events
   :maxdepth: 2



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Features
========

- Discord Bot
- Parses XIVDB
- Handles events (Timezone aware in future)
- Will parse Lodestone
- Will have a music bot portion
- Modular
- Cleverbot integration. If your message has an @mention with the bot's name it will respond. (turns out this was really popular in my FC)

Running
=======

Download the code and change the login details. The bot will automatically respond to any invite you send to it whether in channel or by PM.


Usage
=====

See individual index's for help on each module. You can pull each of them out and use them for your own bot, they're designed to be modular. Cleverbot is built directly into the main bot however. @help now points to this manual hosted on rtfd.

Note that the bot is channel, server and origin agnostic. It responds to each message on teh channel it receives it from. If you PM it an @mention it will respond to you in that PM with a clevebot connection. If you PM it an XIVDB command it will respond in the PM. If you send an invite to a channel on a server it has access to it will treat that invite as any other invite and accept it immediately. Keep this in mind.