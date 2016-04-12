Configuration
=============

So you got an oauth URL from the bot and now need to know how to set this new fangled thing up. Worry not, we can do that. Follow along.

To begin with, all of these commands begin with server. It's the 'this is a server setting' command. Also, all of these commands use @ as their command prefix regardless of settings.

Admin
=====

Setting admin is done per server. You use the following command. Every time you use it the server's admin are set to the symmetric difference between what you provided and the existing list. IE: Items in one or the other but not both.
Bot admin can change server and channel settings including prefix and module loads per channel.

@server admin:[list of name#discriminator]
    Add the list to the server's bot admin. If a name in list is already an admin it will remove then.
    Ex: @server admin:Rory#6028

Prefix
======

You can define a server wide prefix to use besides $. This is mostly for compatibility with other bots. AngelBot is pretty chill, use what you want.

@prefix [thing]
    Set the command prefix to [thing]. That means you would type [thing] before every command in these documents.
    Ex: @server prefix:^

Modules
=======

The bread and butter. By default the bot loads admin onto the server globally. You can then load individual modules. They are named the same thing as they are in these documents for the most part. See below for a list.

List of Modules:
1. AngelEvents
2. XIVDB
3. Admin (You can't remove admin, but you can channel lock it)

So if you wanted to add XIVDB to your server on certain channels you would use:

@server modules:[module]=[list of channels]
    Add XIVDB to your loaded modules. It will respond on any channel in the list of channels.
    Ex: @server modules:XIVDB=Bot-chat Admin FFXIV - Add XIVDB to the Bot-chat, Admin and FFXIV channels on your server

If you wanted to load XIVDB globally:
@server modules:XIVDB
    Add XIVDB to your loaded modules globally. It will respond on all channels in your server that the bot can read.


So the basic command then is:
@server modules:[module][=[channel_list]]
    Where =channel_list is completely optional. Module is the name of a module.