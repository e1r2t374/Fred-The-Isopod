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
#Admin Commands
@fred.command(name="create_react_roles",help="Admin: Command used to create a reaction role channel",usage="<channel name> <roles> <reactions>")
async def create_react_roles(ctx,channel_name: str,roles: str, reactions: str):
    global role_names, react_emojis, message
    if ctx.author.guild_permissions.administrator:
        existing_channel = discord.utils.get(ctx.guild.channels, name=channel_name)
        if existing_channel:
            await ctx.send(f"\"{channel_name}\" already exists")
            return
        role_names = roles.split(',')
        react_emojis = reactions.split(',')
        if len(role_names) != len(react_emojis):
            await ctx.send("Number of roles must match number of reactions")
            return
        channel = await ctx.guild.create_text_channel(channel_name)
        instructions= "React to assign roles:\n"
        for role_name, emoji in zip(role_names, react_emojis):
            role = discord.utils.get(ctx.guild.roles, name=role_name.strip())
            if role:
                    instructions += f"{emoji.strip()} : {role_name.strip()}\n"
            else:
                await ctx.send(f"Role {role_name.strip()} not found. Make sure all roles exist")
                return
        message = await channel.send(instructions)
        for emoji in react_emojis:
            await message.add_reaction(emoji.strip())
        await ctx.send(f"{channel_name} created successfully")
@fred.event
async def on_reaction_add(reaction,user):
    print("reaction added")
    global role_names, react_emojis, message
    if reaction.message == message and user != fred.user:
        for role_name, emoji in zip(role_names, react_emojis):
            if str(reaction.emoji) == emoji:
                role = discord.utils.get(reaction.message.guild.roles, name=role_name.strip())
                if role:
                    await user.add_roles(role)
                    break
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
