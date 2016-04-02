Modules
=======

So you want to add your own module to the bot? You're in the right place. I can help with that. The modules are pretty self explanatory.

Let's just get something out of the way however:

**If it ain't an API, don't ask for it to be merged**

This is an API bot. It interfaces with other APIs. It's focused on this task. I won't accept any random things people throw at it. Thanks.


Format
------

Modules don't really have a set format but they do have five rules. These are as follows.

1. It must have only one class.
2. It must define self.commands which is a list of lists with the format of ['command', function reference].
3. It must accept a redis instance in the __init__
4. Public functions can only accept a discord message object as defined in discord.py
5. Return strings or something other representable object

Let's explain these further.

1. It must have only one class.

My code uses generators to produce the content people interact with. To do that it expects only one class in the file and then creates an instance of that class. If there is more than one class then this causes problems because I can't guarantee the return order of the classes with inspect. I may create an instance of a helper class instead!

2. It must define self.commands.

Self.commands is the bread and butter of your module. You don't have to list every function here, but you do have to list every public function here. So if you have three functions named A, B, C and only A is public, then you would have the following self.commands assuming you want A to activate when someone types [command_prefix]+'dogs.'

self.commands = [['dogs', self.A]]

The generators will handle calling your function and passing the message context to it.

3. It must accept a redis instance in __init__

The bot uses redis for database read and write. It will be passed an aioredis connection pool you should use for all database operations.

4. Public functions can only accept a discord message object as defined in discord.py

Generators require a little bit of sacrifice. Some may say use args and kwargs, sure, but this is better and there's really no reason for any command to ever need more than the message context. Even if I did define args and kwargs, there's no way for the generators to know what your function wants unless I get into heavily abusing inspect which I've no intention of doing.
Bottom line, all functions that expose themselves as commands can only accept a message object. Your function is responsible for doing with that message object what you want.

5. Return strings or something other representable object

It goes without saying that all returns are sent back with send_message. So if it's not a string or an object that returns a human readable str() format then don't return it.


I made one
----------

Oh good, well go to the github page at https://github.com/ccubed/AngelBot and propose a merge. I'll look it over and talk to you then we'll get it added as a default module with all due credit to you.