Configuration
=============

So you got an oauth URL from the bot and now need to know how to set this new fangled thing up. Worry not, we can do that. Follow along.

Admin
-----

Setting admin is done per server. You use the following command. Every time you use it the server's admin are set to the symmetric difference between what you provided and the existing list. IE: Items in one or the other but not both.
Bot admin can change server and channel settings including prefix and module loads per channel.

ardserver admin:[list of mentions]
    Add the list to the server's bot admin. If a name in list is already an admin it will remove then.
    Note: If you have manage_server permissions, you don't need to add yourself to this list. You already are an admin implicitly.
    Ex: ardserver admin:@Rory

Prefix
------

You can define a server wide prefix to use besides $. This is mostly for compatibility with other bots. AngelBot is pretty chill, use what you want.

ardserver prefix:[value]
    Set the command prefix to [value]. That means you would type [value] before every command in these documents.
    Ex: ardserver prefix:^

Modules
-------

The bread and butter. By default the bot loads admin onto the server globally. You can then load individual modules. They are named the same thing as they are in these documents for the most part. See below for a list.

List of Modules:
1. Admin commands are no longer a module. To silence them, just give the bot read permission on a specific channel.
2. See :doc:`APIs`

So if you wanted to add XIVDB to your server on certain channels you would use:

ardserver modules:XIVDBBOT=[list of channels]
    Add XIVDB to your loaded modules. It will respond on any channel in the list of channels (space separated).

If you wanted to load XIVDB globally then you can type: ardserver modules:XIVDB
    Add XIVDB to your loaded modules globally. It will respond on all channels in your server that the bot can read.


So the basic command then is as follows: ardserver modules:[module][=[channel_list]]
    Where =channel_list is completely optional. Module is the name of a module.

As you can see this allows you to configure the bot one of two ways. By using my configuration commands to lock it to channels or by locking it to channels yourself with your read permissions and then adding modules globally. Either works!