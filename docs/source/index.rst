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

Global Commands
===============

These commands always start with an @ and are held in the main bot. There are two currently.

@leave
   If you have the power to kick members, issuing this command to the bot will force it to leave the server. Please note that this will not work in a PM. It needs to be done in a channel on the server you want the bot to leave.

@help
   Sends you a link to this documentation.

@mentions
   Not really a command, but just a reminder that any message with an @mention to the bot's name will have the bot respond to it with a cleverbot generated response.