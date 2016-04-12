Code
====

Nothing in this module is usable by the general public. It exists only for the bot owner and operator Rory#6028. This documentation simply tells you what's going on.


The code module allows hotswapping code and evaluating various python snippets in various contexts within the program.
This is useful because it means:
    1. The bot doesn't have to logoff to update
    2. Debugging is more useful because it has a context
    3. Complex evaluations can be done to test in real time

So basically, don't be surprised if your bot suddenly has new features because it reloaded code. The only code that it can't reload live is the core module, but anything else is fair game.
