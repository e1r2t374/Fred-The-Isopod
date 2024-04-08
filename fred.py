import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.dm_messages=True
intents.guilds=True
fred = commands.Bot(command_prefix='~', intents=intents)

@fred.event
async def on_ready():
    print(f'{fred.user.name} is now Online!')
#Owner Only commands
@fred.command(name="say",help="Owner Only: Command used to send message to TextChannel")
async def say(ctx, destination: discord.TextChannel=None, *, message: str=None):
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

@fred.command(name="dm", help="Owner Only: Command used to send dm without response")
async def dm(ctx, user: discord.Member=None, *, message: str=None):
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

@fred.command(name="msg",help="Owner Only: Command used to send dm with response")
async def msg(ctx, user: discord.Member=None, *, message: str=None):
    if ctx.author.id == ctx.guild.owner_id:
        if user:
            if message:
                try:
                    await user.send(message)
                    await ctx.send(f"\"{message}\" sent to \"{user.mention}\"")
                    def check(message):
                        return message.author == user and message.channel.type == discord.ChannelType.private
                    try:
                        response = await fred.wait_for('message', timeout=180, check=check)
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
