import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.dm_messages = True
intents.guilds = True
fred = commands.Bot(command_prefix = '~', intents = intents)
'''
TODO
- Add Stock market functionality
- Add ai responses to @bot mentions
'''
@fred.event
async def on_ready():
    print(f'{fred.user.name} is now Online!')
#Owner Only commands
@fred.command(name = "say", help = "Owner Only: Send a message to TextChannel as Fred.")
async def say(ctx, destination: discord.TextChannel = None, *, message: str = None):
    if ctx.author.id == ctx.guild.owner_id:
        if destination:
            if message:
                try:
                    await destination.send(message)
                    await ctx.send(f"\"{message}\" sent to \"{destination.mention}\"")
                except Exception as x:
                    await ctx.send(f"Error: {x}")
            else:
                await ctx.send("Specify a Message")
        else:
            await ctx.send("Specify a TextChannel")
    else:
        await ctx.send("You are not my Master!")

@fred.command(name = "dm", help = "Owner Only: Send dm without response as Fred.")
async def dm(ctx, user: discord.Member = None, *, message: str = None):
    if ctx.author.id == ctx.guild.owner_id:
        if user:
            if message:
                try:
                    await user.send(message)
                    await ctx.send(f"\"{message}\" sent to \"{user.mention}\"")
                except Exception as x:
                    await ctx.send(f"Error: {x}")
            else:
                await ctx.send("No Message specified")
        else:
            await ctx.send("No User specified")
    else:
        await ctx.send("You are not my Master!")

@fred.command(name = "msg", help = "Owner Only: Send dm with response as Fred.")
async def msg(ctx, user: discord.Member = None, *, message: str = None):
    if ctx.author.id == ctx.guild.owner_id:
        if user:
            if message:
                try:
                    await user.send(message)
                    await ctx.send(f"\"{message}\" sent to \"{user.mention}\"")
                    def check(message):
                        return message.author == user and message.channel.type == discord.ChannelType.private
                    try:
                        response = await fred.wait_for('message', timeout = 180, check = check)
                        await ctx.send(f"Response from {user.mention}: {response.content}")
                        await user.send("Processing message..")
                    except asyncio.TimeoutError:
                        await ctx.send(f"No response from {user.mention}")
                        await user.send("No response processed")
                except Exception as x:
                    await ctx.send(f"Error: {x}")
            else:
                await ctx.send("Specify a Message")
        else:
            await ctx.send("Specifiy a User")
    else:
        await ctx.send("You are not my Master!")
fred.run('BotToken')
