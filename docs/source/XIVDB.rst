XIVDB
=====

This is the API interface to XIVDB's API. Keep in mind that all of these commands should be prefaced with the command prefix defined for your server or the global command prefix of $.

Commands
========
search [term]
    Search for an item across all available data categories. Will return the number of results matching in each category.

item [name or id]
    Retrieve the details of an item. Name is the name of an item you wish to search for. ID, if you have it, is the numeric ID assigned to the item by XIVDB.

    Example: Maple Lumber

quest [name or id]
    Retrieve the details of a quest. Name is the name of a quest you wish to search for. ID, if you have it, is the numeric ID assigned to the quest by XIVDB.

    Example: Original Sins

recipe [name or id]
    Retrieve the details of a crafting recipe. Name is the name of the craftable item from your crafting log. ID, if you have it, is the numeric ID assigned to the recipe by XIVDB.

    Example: Maple Clogs

action [name or id]
    Retrieve the details of a skill. Name is the name of the skill you want to find. ID, if you have it, is the numeric ID assigned to the skill by XIVDB.

    Example: Convalescence

mats [name or id]
    Retrieve the details of a material you gather. Name is the name of the item you want to gather. ID, if you have it, is the Numeric ID assigned to the material by XIVDB.

    Example: Iron Ore

npc [name or id]
    Retrieve the details of an NPC. Name is the name of the npc you want to find. ID, if you have it, is the Numeric ID assigned to the NPC by XIVDB.

    Note: This method is pretty much impossible to use. XIVDB has one entry for every time an NPC changes positions. For example, there are ~100 alphinauds. I suggest using $quest instead.

    Example: 1016591

effect [name or id]
    Retrieve the details of a status effect. Name is the name of the status effect you want details on. ID, if you have it, is the Numeric ID assigned to it by XIVDB.

    Example: Electroconductivity

minion [name or id]
    Retrieve the details of a minion. Name is the name of the minion you want details on. ID, if you have it, is the Numeric ID assigned to it by XIVDB.

    Example: Cherry Bomb

achievement [name or id]
    Retrieve the details of an achievement. Name is the name of the achievement you want details on. ID, if you have it, is the Numeric ID assigned to it by XIVDB.

    Example: To the Dungeons IV

hdim [name or id]
    Return the recipe for thing. Name is the thing you want to make. ID, if you have it, is the Numeric ID assigned by XIVDB. This is a utility function. It's equivalent to $recipe.

    Example: Maple Clogs

wdif [name or id]
    Where do I find thing. Name is what you want to find. ID, if you have it, is the Numeric ID assigned by XIVDB. This will tell you all the ways you can find thing.

    Example: Curtana