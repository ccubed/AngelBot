.. AngelBot documentation master file, created by
   sphinx-quickstart on Mon Apr  4 20:25:30 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to AngelBot's documentation!
====================================

.. toctree::
   Configuration
   APIs
   Misc
   Security


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Features
========

- Discord Bot
- Modular (It's easy for others to add functionality)
- Per Server Prefixes
- Supports Oauth flows in various APIs

What is this
============

A discord bot called AngelBot. AngelBot started as a FFXIV bot but has steadily grown into a complicated, sophisticated API machine. Currently it supports AniList, XIVDB, Overwatch Stats, Riot's League of Legends API, Fixer.io and XKCD.

Running
=======

Well with the new API you no longer need a locally running copy. If you DM the bot, it assumes you want an Oauth link to the addbot flow and will respond with that. So to get the bot going on your server send a DM to AngelBot#7020.


Usage
=====

Once the bot joins the server all commands are enabled by default with a prefix of $. You can define a prefix using the ardserver prefix:<prefix> command. AngelBot supports pretty much anything as a prefix, even emojis.

Global Commands
===============

@AngelBot Help


@AngelBot Info


PM AngelBot Oauth