from http import client
import random
import discord
from discord.ext import commands, tasks
from itertools import cycle

client = commands.Bot(command_prefix= ".")

@client.event
async def on_ready():
    update_status.start()
    print("Bot is ready!")

status = cycle(["Spreading cuteness!", "Meowing"])
@tasks.loop(seconds=10)
async def update_status():
    await client.change_presence(activity = discord.Game(next(status)))


@client.command()
async def ping(ctx):
    await ctx.send(f"{round(client.latency * 1000)}")

@client.command(aliases = ["8ball"])
async def eightball(ctx, *, q):
    responses = ["It is certain",
     "It is decidedly so", 
     "Without a doubt", 
     "Yes. definitely", 
     "You may rely on it", 
     "As I see it, yes", 
     "Most likely", 
     "Outlook good", 
     "Yes", 
     "Signs point to yes", 
     "Reply hazy, try again", 
     "Ask again later", 
     "Better not tell you now", 
     "Cannot predict now", 
     "Concentrate and ask again", 
     "Don't count on it", 
     "My reply is no", 
     "My sources say no", 
     "Outlook not so good", 
     "Very doubtful"]

    await ctx.send(random.choice(responses))

@client.command()
@commands.has_permissions(manage_messages = True)
async def delete(ctx, amount = 1):
    await ctx.channel.purge(limit = amount + 1)
    if amount < 0:
        await ctx.send("You have to delete at least one message.")

@client.command()
@commands.has_permissions(manage_messages = True)
async def kick(ctx, member : discord.Member):
    await member.kick(reason=None)

@client.command()
@commands.has_permissions(manage_messages = True)
async def ban(ctx, member : discord.Member, *, reason = None):
    await member.ban(reason = reason)

@client.command()
@commands.has_permissions(manage_messages = True)
async def unban(ctx, *, member):
    banned_members = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for i in banned_members:
        if (i.user.name , i.user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(i.user)
            await ctx.send("Member unbanned!")
            break

@client.command()
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")

@eightball.error
async def eightball_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Where the question?")

client.run("MTAwMjk0MTE3MzQ2MTE2NDA1Mg.GubsaW.-9SvGEt2J8W0BTYs5m0Nbvu4_kEwW59t2NA6nc")