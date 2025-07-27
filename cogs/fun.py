from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self, datastore, emojis):
        self.datastore = datastore
        self.emojis = emojis

    @commands.command(
        help = "Play a game of russian roulette.",
        aliases = ["rrl"]
    )
    async def russianroulette(self, ctx):
        #self.datastore.change(str(ctx.author.id), "coins_wallet", 0, "=")

        await ctx.reply("In development") 