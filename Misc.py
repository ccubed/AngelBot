from random import randint
from discord import embeds

class Misc:
    """
    This class handles miscellaneous commands that don't belong elsewhere.
    """
    def __init__(self, client):
        self.bot = client
        self.commands = [['roll', self.dice], ['rtd', self.dice]]

    async def dice(self, message):
        """
        Roll some dice for the user with an optional reason.

        :param message: a discord.py Message object
        """
        dstr = message.content.split()[1]
        if 'd' not in dstr:
            await self.bot.send_message(message.channel, "Use this command like: <prefix>roll xdy <reason>")

        if dstr.split('d')[0] == '':
            dice = 1
            try:
                int(dstr.split('d')[1])
            except ValueError:
                await self.bot.send_message(message.channel, "Number of sides on the dice must be a number.")
                return
        else:
            try:
                dice, sides = int(dstr.split('d')[0]), int(dstr.split('d')[1])
            except ValueError:
                await self.bot.send_message(message.channel, "Number of sides and number of dice must be a number.")
                return

        results = []
        for die in range(dice):
            results.append(randint(1, sides))

        reason_msg = None
        if len(message.split()) > 2:
            reason_msg = " ".join(message.content.split()[2:])

        if reason_msg:
            embed = embeds.Embed(description=reason_msg)
        else:
            embed = embeds.Embed()
        embed.title = "Rolled dice for {}".format(message.author)
        embed.add_field(name="Number Rolled", value=dice)
        embed.add_field(name="Type of Dice", value="d{}".format(sides))
        embed.add_field(name="Dice Rolls", value=" ".join(results))
        embed.add_field(name="Sum of Rolls", value=sum(results))
        await self.bot.send_message(message.channel, embed=embed)