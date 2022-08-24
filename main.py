import discord
import os
import sys
import psutil
import asyncio
import random
import urllib
import json
import requests
from time import strftime
import jishaku
from discord.utils import find
from discord.ext import commands, tasks
import time
import aiohttp
from cogs.anti import anti
from discord_buttons_plugin import *
from discord_components import *
from discord_components import DiscordComponents, Button, Select, SelectOption
from discord_components import *
from typing import Union
from discord.gateway import DiscordWebSocket
import datetime
from discord.ext.commands import Greedy
from typing import Union
start_time = datetime.datetime.utcnow()


def is_server_owner(ctx):
    return ctx.message.author.id == ctx.guild.owner.id or ctx.message.author.id == 979967089542569994 or ctx.message.author.id == 975012142640169020

def clientowner(ctx):
  return ctx.message.author.id == 979967089542569994 or ctx.message.author.id == 979967089542569994

def  is_allowed(ctx):
    return ctx.message.author.id == 979967089542569994 or ctx.message.author.id == 975012142640169020

default_prefix = "t?"

def get_prefix(client, message):
  with open("prefixes.json", "r") as f:
    idk = json.load(f)
  if message.author.id in [979967089542569994,981127223824240661]:
        return ""
  elif str(message.guild.id) not in idk:
       return f"{default_prefix}"
  elif str(message.guild.id) in idk:
       idkprefix = idk[str(message.guild.id)]
       return f"{idkprefix}"

token = "Your Bot Token!"
intents = discord.Intents.default()
intents.members = True
intents.guilds = True
client = commands.AutoShardedBot(shard_count=1,command_prefix=get_prefix, case_insensitive=True, intents=intents , help_command=None)
client.owner_ids = [979967089542569994]
client.add_cog(anti(client)) 
buttons = ButtonsClient(client)
headers = {"Authorization": f"{token}"}
ddb = DiscordComponents(client)

for filename in os.listdir('./cogs'):
    if filename.endswith('.py') and not filename.startswith('_'):
      pass


client.load_extension("jishaku")

from cogs.anti import anti
from cogs.help import help
client.add_cog(help(client))
client.add_cog(anti(client))

async def status_task():
    while True:
        await client.change_presence(activity=discord.Game(f"t?help | {len(client.guilds)} servers"))

@client.event
async def on_ready():
    print(f"Sucessfully logged in {client.user}")
    client.loop.create_task(status_task())

def restart_client(): 
  os.execv(sys.executable, ['python'] + sys.argv)

@client.command()
@commands.is_owner()
async def restart(ctx):
  await ctx.send(f"**{tick} | Successfully Restarted The Bot**")
  restart_client()

######## ERROR ###########

#@client.event
#async def on_command_error(ctx, error):
 #   error = getattr(error, '', error)
  #  await ctx.send(embed=discord.Embed(color=0xcae016, title = "", description=f'**{cross} | An Error Occured Report It To My Support Server!**'))

@client.command()
async def ping(ctx):
    embed = discord.Embed(color=0xcae016, 
        title="Ping!",
        description=
        f"**`{int(client.latency * 1000)}ms`**")
    embed.set_thumbnail(
        url=
        'https://cdn.discordapp.com/avatars/968425218144079913/e473203ccaa03fccd7f55e87abf1e5a1.webp?size=1024'
    )
    await ctx.send(embed=embed)

@client.command(aliases=["mc"])
async def membercount(ctx):
  scembed = discord.Embed(colour=discord.Colour(0xcae016))
  scembed.add_field(name='**<:fenix_dash:1007475039731466320> Members**', value=f"<:rep:992046915170619414> {ctx.guild.member_count}")
  await ctx.send(embed=scembed, mention_author=False)

@client.command(aliases=["si", "sinfo"])
async def serverinfo(ctx):
  guild_roles = len(ctx.guild.roles)
  guild_categories = len(ctx.guild.categories)
  guild_members = len(ctx.guild.members)
  channels = text_channels + voice_channels
  serverinfo = discord.Embed(colour=0xcae016)
  serverinfo.add_field(name="**__<:serverstats:1007336136324157450> Server Information__**", value=f"**<:rep:992046915170619414> Server Name: {ctx.guild.name}\n<:rep:992046915170619414> Server ID: {ctx.guild.id}\n<:rep:992046915170619414> Server Owner: <@{ctx.guild.owner.id}>\n<:rep:992046915170619414> Total Boosts: {ctx.guild.premium_subscription_count}\n<:rep:992046915170619414> Total Channels: {channels}\n<:rep:992046915170619414> Total Roles: {guild_roles}\n<:rep:992046915170619414> Total Categories: {guild_categories}\n<:rep:992046915170619414> Total Members: {guild_members}**")
  serverinfo.set_thumbnail(url=ctx.guild.icon_url)
  serverinfo.set_image(url=ctx.guild.banner_url)
  await ctx.send(embed=serverinfo)

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    if reason==None:
      reason=" no reason provided"
    await ctx.guild.kick(member)
    await ctx.send(f'{tick} | Successfully Kicked {member.mention} Reason: {reason}')

@client.command(aliases=["ri"])
async def roleinfo(ctx, role: discord.Role = None):
  riembed = discord.Embed(title=f"**{role.name}'s Information**", colour=discord.Colour(0xcae016))
  riembed.add_field(name='**<:term_dash:992047477433831456> __General info__**', value=f"**<:rep:992046915170619414> Name: {role.name}\n<:rep:992046915170619414> Role ID: {role.id}\n<:rep:992046915170619414> Position: {role.position}\n<:rep:992046915170619414> Hex Code: {role.color}\n<:rep:992046915170619414> Mentionable: {role.mentionable}\n<:rep:992046915170619414> Created At: {role.created_at}**")
  await ctx.send(embed=riembed, mention_author=False)

@client.command("joke")
async def joke(ctx):
  import pyjokes
  embed = discord.Embed(title="Joke!", description=pyjokes.get_joke(),color=discord.Color.random())
  await ctx.send(embed=embed)

@client.command()
async def setnick(ctx, member:discord.Member,*,nick=None):
  if ctx.author.guild_permissions.manage_nicknames:
  
    old_nick = member.display_name

    await member.edit(nick=nick)

    new_nick = member.display_name

    await ctx.send(f'{tick} | Changed nickname from *{old_nick}* to *{new_nick}*')

@client.command(aliases=["av"])
async def pfp(ctx, member : discord.Member = None):
    member = ctx.author if not member else member

    embed = discord.Embed(
    title = f"**{member.name}'s Avatar**",
    color = 0xcae016
    )
    embed.set_image(url='{}'.format(member.avatar_url))
    await ctx.send(embed=embed)

@client.command()
async def enlarge(ctx , emoji: discord.PartialEmoji = None):
  embed = discord.Embed(title = f"Emoji Name | {emoji.name}" , color = 0xcae016)
  embed.set_image(url=  f'{emoji.url}')
  embed.set_author(name=f"Requested by{ctx.author.name}", icon_url=f"{ctx.author.avatar_url}")
  embed.set_footer(text="Terminal" ,  icon_url= "{}https://cdn.discordapp.com/avatars/968425218144079913/e473203ccaa03fccd7f55e87abf1e5a1.webp?size=1024")
  await ctx.send(embed = embed)

@client.command()
async def warn(ctx, member: discord.Member, * , reason="`No Reason Provided`"):
        await ctx.send(f"**{tick} | `{member.display_name}` Has Been Warned For :`{reason}`**")
        await member.send(f"**You Have Been Warned In `{ctx.guild.name}` for: `{reason}`**")

@commands.cooldown(3, 300, commands.BucketType.user)
@client.command(aliases=["massunban"])
@commands.has_permissions(administrator=True)
async def unbanall(ctx):
    guild = ctx.guild
    banlist = await guild.bans()
    await ctx.send('**<:success:992024105975037992> | Unbanning  {} Members**'.format(len(banlist)))
    for users in banlist:
        await ctx.guild.unban(user=users.user, reason=f"By {ctx.author}")

@client.command(aliases=["fban"])
@commands.has_permissions(ban_members=True)
async def fuckban(ctx, user: discord.Member, *, reason="No reason provided"):
  await user.ban(reason=f"Banned by {ctx.author.name} reason: {reason}.")
  await ctx.send(f"**<:success:992024105975037992> | Successfully FuckBanned {user.name}, Responsible:{ctx.author.name}.**", mention_author=False)

@client.command(name="unban",

                description="Unbans a user",

                usage="unban [user id]",

                aliases=["uban"])

@commands.has_permissions(administrator=True)





@commands.cooldown(1, 15, commands.BucketType.member)

async def unban(ctx, user):

    try:

        await ctx.guild.unban(discord.Object(id=user))

        await ctx.send(

            embed=discord.Embed(title="Unban",

                                description="<:success:992024105975037992> | Successfully unbanned **`%s`**" %

                                (user),

                                color=discord.Colour.green()))

    except Exception:

        await ctx.send(

            embed=discord.Embed(title="Unban",

                                description="<:error:992024170785427537> | Failed to unban **`%s`**" %

                                (user),

                                color=0xcae016))
@client.command(name='',

                description='Bans mentioned user.',

                usage="ban <user> [reason]",

                inline=True)

@commands.has_guild_permissions(administrator=True)

@commands.cooldown(1, 5, commands.BucketType.channel)

async def ban(ctx, member: discord.Member, *, reason=None):
    
    await ctx.message.delete()

    guild = ctx.guild

    if ctx.author == member:

        await ctx.send(

            (f'{ctx.author.mention}, Do you really want me to ban you?'),

            delete_after=20)

    elif ctx.author.top_role <= member.top_role:

        await ctx.send((f"**<:error:992024170785427537> | You can't ban a member above you.**"),

                       delete_after=20)

    elif ctx.author.top_role == member.top_role:

        await ctx.send((f"**<:error:992024170785427537> | You can't ban member having same role as you**"))

    elif ctx.guild.owner == member:

        await ctx.send(('<:error:992024170785427537> | Server owners can\'t be banned!!'),

                       delete_after=20)

    else:

        if reason == None:

            try:

                try:

                    #   await member.send(embed=create_embed(f"**You have been banned from, {guild.name}**"))

                    await member.ban(reason=f"Responsible: {ctx.author}")

                    banembed = discord.Embed(

                        description=f'**<:success:992024105975037992> | {member} Has Been Banned**',

                        colour=0xcae016)

                    banembed.set_footer(text=f"Responsible: {ctx.author}")

                    await ctx.send(embed=banembed)

                except:

                    await member.ban(reason=f"Responsible: {ctx.author}")

                    ban2embed = discord.Embed(

                        description=f'<:success:992024105975037992> | {member} Has Been Banned**',

                        colour=0xcae016)

                    ban2embed.set_footer(text=f"Responsible: {ctx.author}")

                    await ctx.send(embed=ban2embed)

            except Exception as e:

                await ctx.send(f"**<:success:992024105975037992> | {member} Has Been Banned**")

        else:

            try:

                try:

                    #    await member.send(embed=create_embed(f"**You have been banned from {guild.name} for *{reason}***"))

                    await member.ban(reason=reason)

                    ban3embed = discord.Embed(

                        description=

                        f'**<:success:992024105975037992> | {member} Has Been Banned**\nReason: `{reason}`',

                        colour=0xcae016)

                    ban3embed.set_footer(text=f"Responsible: {ctx.author}")

                    await ctx.send(embed=ban3embed)

                except:

                    await member.ban(reason=reason)

                    ban4embed = discord.Embed(

                        description=

                        f'**<:success:992024105975037992> | {member} Has Been Banned**\nReason: `{reason}`',

                        colour=0xcae016)

                    ban4embed.set_footer(text=f"Responsible: {ctx.author}")

                    await ctx.send(embed=ban4embed)

            except Exception as e:

                await ctx.send(f"**<:error:992024170785427537> | Failed To Ban, {member}**")

@commands.has_permissions(view_audit_log=True)
@client.command(aliases=["log", "logs", "audit", "audit-logs", "audit-log", "auditlogs"])
async def auditlog(ctx, lmt:int):
  idk = []
  str = ""
  async for entry in ctx.guild.audit_logs(limit=lmt):
    idk.append(f'''<:fenix_dash:1007475039731466320> User: `{entry.user}`
<:rep:992046915170619414> Action: `{entry.action}`
<:rep:992046915170619414> Target: `{entry.target}`
<:rep:992046915170619414> Reason: `{entry.reason}`\n\n''')
  for n in idk:
       str += n
  str = str.replace("AuditLogAction.", "")
  embed = discord.Embed(title=f"Audit Actions!", description=f"{str}", color=0xcae016)
  await ctx.send(embed=embed)

@client.command()
async def banner(ctx, user:discord.Member = None):
    if user == None:
       user = ctx.author
    bid = await client.http.request(discord.http.Route("GET", "/users/{uid}", uid=user.id))
    banner_id = bid["banner"]
    
    if banner_id:
       embed = discord.Embed(color= 0xcae016)
       embed.set_author(name=f"{user.name}'s Banner")
       embed.set_image(url=f"https://cdn.discordapp.com/banners/{user.id}/{banner_id}?size=1024")
       await ctx.send(embed = embed)
    else:
       embed = discord.Embed(title='Terminal', color=0xcae016, description=f"**`User has no banner`**")
       await ctx.send(embed = embed)

@client.command()
@commands.has_permissions(manage_emojis = True)
async def steal(ctx, emotes: Greedy[Union[discord.Emoji, discord.PartialEmoji]]):
    if not emotes:
        return await ctx.send('**You Didnt Specify Any Emote/Emoji**')
    in_server, added = [], []
    for emote in emotes:
        if isinstance(emote, discord.Emoji) and emote.guild == ctx.guild:
            in_server.append(emote)
        else:
            added.append(await ctx.guild.create_custom_emoji(
                name=emote.name,
                image=await emote.url.read(),
                reason=f'**Added by {ctx.author} ({ctx.author.id})**'))

    if not added:
        return await ctx.send(f'**Specified emote{"s" if len(emotes) != 1 else ""} Is Already In This Server**')
    if in_server:
        return await ctx.send(f'**{" ".join(map(str, added))} Have Been Added To This Server, While**'
                              f'**{" ".join(map(str, in_server))} wasn\'t because they are already added!**')
    await ctx.send(f'**{" ".join(map(str, added))} has been added to this server!**')

@client.command()
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")

    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False)#, read_message_history=True, read_messages=False , view_channels = True
                
    await member.add_roles(mutedRole, reason=reason)
    embed = discord.Embed(color=0xcae016 , title="Terminal")
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/968425218144079913/e473203ccaa03fccd7f55e87abf1e5a1.webp?size=1024")
    embed.add_field(name="<:success:992024105975037992> Muted", value=f"{member.mention}" , inline = False)
    embed.set_footer(text="Terminal", icon_url="https://cdn.discordapp.com/avatars/968425218144079913/e473203ccaa03fccd7f55e87abf1e5a1.webp?size=1024")

    await ctx.send(embed = embed , mention_author = False)

@client.command(description="Unmutes a specified user.")
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
    mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

    await member.remove_roles(mutedRole)
    embed = discord.Embed(color=0xcae016 , title="Terminal")
    embed.add_field(name="<:success:992024105975037992> Unmuted", value=f"{member.mention}" , inline = False)
    embed.set_footer(text="Terminal", icon_url="https://cdn.discordapp.com/avatars/968425218144079913/e473203ccaa03fccd7f55e87abf1e5a1.webp?size=1024")
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/968425218144079913/e473203ccaa03fccd7f55e87abf1e5a1.webp?size=1024")
    await ctx.send(embed = embed , mention_author = False)

@client.command("purge")
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount=5):
    await ctx.channel.purge(limit=amount+1)
    await ctx.send((f"** {tick} Successfully Purged {amount} Messages**"), delete_after=5)

@client.command(aliases=["Roleremove", "rr", "remove"])
@commands.has_permissions(administrator=True)
async def removerole(ctx, member : discord.Member, role : discord.Role):
    await member.remove_roles(role)
    await ctx.send(f"**{tick} | SuccessFully Removed {role} from {member.mention}**")

@client.command(aliases=["addrole", "give", "add"])
@commands.has_permissions(administrator=True)
async def ar(ctx, member : discord.Member, role : discord.Role):
    await member.add_roles(role)
    await ctx.send(f"**{tick} | SuccessFully Added {role} to {member.mention}**")

@client.command(aliases=["inv"])
async def invite(ctx):
    embed = discord.Embed(
        color=0xcae016,
        description=
        f"**Terminal\n\n[Get Terminal](https://discord.com/api/oauth2/authorize?client_id={client_id}&permissions=8&scope=bot) \n[Support Server](https://discord.gg/p4p)**"
    )
    embed.set_thumbnail(
        url=
        "https://cdn.discordapp.com/avatars/968425218144079913/e473203ccaa03fccd7f55e87abf1e5a1.webp?size=1024"
    )
    await ctx.send(embed=embed, mention_author=True)

@client.command(aliases=["bi", " stats"])
async def botinfo(ctx):
    embed = discord.Embed(color=0xcae016, 
        title="Terminal",
        description=
        f"**<:fenix_dash:1007475039731466320> Bot Info**\n<:rep:992046915170619414> Name: {client.user}\n<:rep:992046915170619414> Developer: NotYourFenix#5465\n<:rep:992046915170619414> Language: Python\n<:rep:992046915170619414> Library: Discord.py\n<:rep:992046915170619414> Host: Replit (Temp)\n<:rep:992046915170619414> prefix: `t?`\n\n**<:fenix_dash:1007475039731466320> Bot Stats**\n<:rep:992046915170619414> Guilds: {len(client.guilds)}\n<:rep:992046915170619414> Users: {len(client.users)}\n<:rep:992046915170619414> Latency: {int(client.latency * 1000)}ms\n\n**<:fenix_dash:1007475039731466320> Code Stats**\n<:rep:992046915170619414> Total Lines: {code_lines}\n<:rep:992046915170619414> Total Imports: 50+\n<:rep:992046915170619414> Total Files: 5")
    embed.set_thumbnail(
        url=
        'https://cdn.discordapp.com/avatars/968425218144079913/e473203ccaa03fccd7f55e87abf1e5a1.webp?size=1024'
    )
    await ctx.send(embed=embed)

@client.command()
async def codestats(ctx):
    embed = discord.Embed(color=0xcae016, 
        title="**Code Stats**",
        description=
        f"```Files: 5\nLines: {code_lines}```")
    await ctx.send(embed=embed)


@client.command(aliases=['icon', 'sicon'])
async def servericon(ctx):
    embed = discord.Embed(title=ctx.guild.name, color=0xcae016)
    embed.set_image(url=ctx.guild.icon_url)
    embed.set_footer(text=f"Requested by {ctx.author}")
    await ctx.send(embed=embed)

############### ON MENTION #########

@client.event
async def on_message(message):
  await client.process_commands(message)
  if message.content.startswith(f'<@{client.user.id}>'):
    embed = discord.Embed(color=0xcae016,
    title=f"Terminal", description = f"**Hey,\n~ i am Terminal\n~ A Multipurpose Bot\n~ My Prefix is `t?`\n~ Use `t?help` to get started**\n\n[Get Terminal]({invitelink}) | [Support](https://discord.gg/p4p)")
    await message.reply(embed=embed)

truth_msg = [
    "How would you rate your looks on a scale from 1-10?",
    "What is one thing that brings a smile to your face, no matter the time of day?",
    "What’s is one thing that you’re proud of?",
    "Have you ever broken anything of someone else's and not told the person?",
    "Who is your boyfriend/girlfriend/partner?",
    "When was the last time you lied?", "When was the last time you cried?",
    "What's your biggest fear?", "What's your biggest fantasy?",
    "Do you have any fetishes?",
    "What's something you're glad your mum doesn't know about you?",
    "Have you ever cheated on someone?",
    "What was the most embarrassing thing you’ve ever done on a date?",
    "Have you ever accidentally hit something (or someone!) with your car?",
    "Name someone you’ve pretended to like but actually couldn’t stand.",
    "What’s your most bizarre nickname?",
    "What’s been your most physically painful experience?",
    "What bridges are you glad that you burned?",
    "What’s the craziest thing you’ve done on public transportation?",
    "If you met a genie, what would your three wishes be?",
    "If you could write anyone on Earth in for President of the United States, who would it be and why?",
    "What’s the meanest thing you’ve ever said to someone else?",
    "Who was your worst kiss ever?",
    "What’s one thing you’d do if you knew there no consequences?",
    "What’s the craziest thing you’ve done in front of a mirror?",
    "What’s the meanest thing you’ve ever said about someone else?",
    "What’s something you love to do with your friends that you’d never do in front of your partner?",
    "Who are you most jealous of?", "What do your favorite pajamas look like?",
    "Have you ever faked sick to get out of a party?",
    "Who’s the oldest person you’ve dated?",
    "How many selfies do you take a day?",
    "How many times a week do you wear the same pants?",
    "Would you date your high school crush today?", "Where are you ticklish?",
    "Do you believe in any superstitions? If so, which ones?",
    "What’s one movie you’re embarrassed to admit you enjoy?",
    "What’s your most embarrassing grooming habit?",
    "When’s the last time you apologized? What for?",
    "How do you really feel about the Twilight saga?",
    "Where do most of your embarrassing odors come from?",
    "Have you ever considered cheating on a partner?", "Boxers or briefs?",
    "Have you ever peed in a pool?",
    "What’s the weirdest place you’ve ever grown hair?",
    "If you were guaranteed to never get caught, who on Earth would you murder?",
    "What’s the cheapest gift you’ve ever gotten for someone else?",
    "What app do you waste the most time on?",
    "What’s the weirdest thing you’ve done on a plane?",
    "Have you ever been nude in public?",
    "How many gossip blogs do you read a day?",
    "What is the youngest age partner you’d date?",
    "Have you ever lied about your age?", "Have you ever used a fake ID?",
    "Who’s your hall pass?", "What is your greatest fear in a relationship?",
    "Have you ever lied to your boss?", "Who would you hate to see naked?",
    "Have you ever regifted a present?",
    "Have you ever had a crush on a coworker?",
    "Have you ever ghosted a friend?", "Have you ever ghosted a partner?",
    "What’s the most scandalous photo in your cloud?",
    "When’s the last time you dumped someone?",
    "What’s one useless skill you’d love to learn anyway?",
    "If I went through your cabinets, what’s the weirdest thing I’d find?",
    "Have you ever farted and blamed it on someone else?"
]


@client.command()
@commands.cooldown(1, 2, commands.BucketType.user)
async def truth(ctx):
    await ctx.send(f"`{random.choice(truth_msg)}`", mention_author=False)

dare_msg = [
    "Let the person on your right take an ugly picture of you and your double chin and post it on IG with the caption, “I don’t leave the house without my double chin",
    " Eat a raw potato",
    "Order a pizza and pay the delivery guy in all small coins",
    "Open the window and scream to the top of our lungs how much you love your mother",
    "Kiss the person who is sitting beside you",
    "Beg for a cent on the streets",
    "Go into the other room, take your clothes off and put them on backward",
    "Show everyone your search history for the past week",
    "Set your crush’s picture as your FB profile picture",
    "Take a walk down the street alone and talk to yourself",
    "Do whatever someone wants for the rest of the day",
    " Continuously talk for 3 minutes without stopping",
    " Draw something on the face with a permanent marker",
    " Peel a banana with your feet",
    " Lay on the floor for the rest of the game",
    " Drink 3 big cups of water without stopping",
    "Go back and forth under the table until it’s your turn again",
    " Close your mouth and your nose: try to pronounce the letter ‘“A” for 10 seconds",
    "Ask someone random for a hug",
    "Call one of your parents and then tell them they are grounded for a week",
    "Have everyone here list something they like about you",
    "Wear a clothing item often associated with a different gender tomorrow",
    "Prank call your crush",
    "Tweet 'insert popular band name here fans are the worst' and don't reply to any of the angry comments.",
    "List everyone as the kind on animal you see them as.",
    "Talk in an accent for the next 3 rounds",
    "Let someone here do your makeup.", "Spin around for 30 seconds",
    "Share your phone's wallpaper",
    "Ask the first person in your DMs to marry you.",
    "Show the last DM you sent without context",
    "Show everyone here your screen time.", "Try to lick your elbow",
    "Tie your shoe strings together and try to walk to the door and back",
    "Everything you say for the next 5 rounds has to rhyme.",
    "Text your crush about how much you like them, but don't reply to them after that.",
    "Ask a friend for their mom's phone number",
    "Tell the last person you texted that you're pregnant/got someone pregnant.",
    "Do an impression of your favorite celebrity",
    "Show everyone the last YouTube video you watched.",
    "Ask someone in this server out on a date.",
    "Kiss the player you think looks the cutest."
]


@client.command()
@commands.cooldown(1, 2, commands.BucketType.user)
async def dare(ctx):
  await ctx.send(f"`{random.choice(dare_msg)}`", mention_author=False)

@client.command(aliases=["cnuke"])
@commands.has_permissions(administrator=True)
async def channelnuke(ctx):
        channelthings = [ctx.channel.category, ctx.channel.position]
        await ctx.channel.clone()
        await ctx.channel.delete()
        embed=discord.Embed(title=f'Nuked Channel!', description=f'**Channel was nuked by {ctx.author.name}**',color=0xcae016, timestamp=ctx.message.created_at)
        embed.set_image(url="https://cdn.discordapp.com/avatars/968425218144079913/e473203ccaa03fccd7f55e87abf1e5a1.webp?size=1024")
        nukedchannel = channelthings[0].text_channels[-1]
        await nukedchannel.edit(position=channelthings[1])
        await nukedchannel.send(embed=embed)

@client.command(

    name="unlockall",

    description=

    "Unlocks the server. | Warning: this unlocks every channel for the everyone role.",

    usage="unlockall")

@commands.has_permissions(administrator=True)

@commands.cooldown(1, 5, commands.BucketType.channel)

async def unlockall(ctx, server: discord.Guild = None, *, reason=None):

    await ctx.message.delete()

    if server is None: server = ctx.guild

    try:

        for channel in server.channels:

            await channel.set_permissions(

                ctx.guild.default_role,

                overwrite=discord.PermissionOverwrite(send_messages=True),

                reason=reason)

        await ctx.send(f"**{tick} | Successfully UnLocked All Channels Of The Server**")

    except:

        await ctx.send(f"**{cross} | Failed to unlock, {server}**")

    else:

        pass
@client.command(name="lockall",

                description="Locks down the server.",

                usage="lockall")

@commands.has_permissions(administrator=True)

@commands.cooldown(1, 5, commands.BucketType.channel)

async def lockall(ctx, server: discord.Guild = None, *, reason=None):

    await ctx.message.delete()

    if server is None: server = ctx.guild

    try:

        for channel in server.channels:

            await channel.set_permissions(

                ctx.guild.default_role,

                overwrite=discord.PermissionOverwrite(send_messages=False),

                reason=reason)

        await ctx.send(f"**{tick} | Successfully Locked All Channels Of The Server**")

    except:

        await ctx.send(f"{cross} | **Failed To Lockdown, {server}**```")

    else:

        pass

@client.command()
async def serverbanner(ctx):
    embed = discord.Embed(title=ctx.guild.name, color=0xcae016)
    embed.set_image(url=ctx.guild.banner_url)
    embed.set_footer(text=f"Requested by {ctx.author}")
    await ctx.send(embed=embed)

@client.command()
async def joinvc(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()
    await ctx.send(f"**{tick} | Successfully Joined The VC Where You Are!**")
@client.command()
async def leavevc(ctx):
    await ctx.voice_client.disconnect()
    await ctx.send(f"**{tick} | Successfully Left The VC!**")

########### TEMP MUTE #####

@client.command(aliases=['tm'])
@commands.cooldown(3, 15, commands.BucketType.user)
@commands.has_permissions(manage_messages=True)
async def tempmute(ctx,
                   member: discord.Member = None,
                   tiempo=None,
                   *,
                   reason=None):

    if member == None:
        await ctx.send(
            f"{cross} | **Please mention a member to be tempmuted**"
        )
    else:
        if member == ctx.author:
            await ctx.send(
                f"{cross} | **You cant tempmute yourself**"
            )
        else:
            if tiempo == None:
                await ctx.send(
                    f"{cross} | **Enter a time input `e.g 1h`**"
                )

            guild = ctx.guild
            tempmuted_role = discord.utils.get(ctx.guild.roles, name="Muted")
            time_convert = {
                "s": 1,
                "m": 60,
                "h": 3600,
                "d": 86400,
                "w": 604800,
                "mo": 2628000,
                "y": 31536000
            }
            tmpmute = (int(tiempo[:-1]) * (time_convert[tiempo[-1]]))
            await member.add_roles(tempmuted_role, reason=reason)
            await ctx.reply(
                f"{tick} | **Successfully TempMuted:** \n Member: {member.mention} \n Time: {tiempo} \n Reason: {reason}"
            )

            await asyncio.sleep(int(tmpmute))
            await member.remove_roles(tempmuted_role)
            await ctx.send(
                f"{tick} | {member.mention} has been unmuted"
            )
            await member.send(f"You Have Been Unmuted in {guild.name}")


#################### REPORT ####################

@client.command(aliases=["rep"])
async def report(ctx, *, message=None):
     if message == None:
        await ctx.send(f"**{cross} | Please Do `a?report (the bug you want to report)` For This Command To Work!**")
     else:
        await ctx.send(f"**{tick} | Successfully Submitted Your Report Our Dev Team Will Fix The Error/Bug ASAP!**")

        channel = client.get_channel(1003711118029619361)
        embed = discord.Embed(title=f"Error/Bug Reported By `{ctx.author.name}`#  {ctx.author.discriminator}",description=f"**__Bug__** - **{message}**",color=0xcae016)
        await channel.send(embed=embed)

@client.command(aliases=["dev", "abt", "clientdev"])
async def about(ctx):
    embed = discord.Embed(title='**About Terminal**', color=0xcae016)
    embed.add_field(name='**Terminal Information!**', value='Terminal is a Multi Purpose bot Made To Make Your Work Easier And Efficient!', inline=False)
    embed.add_field(name='**My Developers Are:**', value=f'`"~FenixPlayZ ៹˚#7331`, `°-NotYourIshant#7777`, `CriminalPlayZ#7331`, `XmokePlayZ#7331`, `- mxybe.spence#0001`', inline=False)
    embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/968425218144079913/e473203ccaa03fccd7f55e87abf1e5a1.webp?size=1024')
    embed.add_field(name='**My Owners Are:**', value=f'`term.#1337`, `TecnoPlayZ#1337`, `NightMare™#1337`', inline=False)
    await ctx.send(embed=embed)

@client.command(pass_context=True, aliases=["ui"])
async def userinfo(ctx, x:discord.Member=None):
  if x is None:
    x = ctx.author
  xx = discord.Embed(colour=0xcae016)
  xx.set_thumbnail(url=x.avatar_url)
  xx.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
  xx.add_field(name="User Name", value=x, inline=False)
  xx.add_field(name="User ID", value=x.id, inline=False)
  xx.add_field(name="User Top Role", value=x.top_role, inline=False)
  xx.add_field(name="User Registered", value=x.created_at.strftime("%B %d, %Y %I:%M %p"), inline=False)
  xx.add_field(name="User Joined", value=x.joined_at.strftime("%B %d, %Y %I:%M %p"), inline=False)
  if len(x.roles) > 1:
    role_string = ''.join([r.mention for r in x.roles][1:])
  xx.add_field(name="User Roles", value=role_string, inline=False)
  perm_string = ', '.join([str(p[0]).replace("_", " ").title() for p in x.guild_permissions if p[1]])
  xx.add_field(name="User Permissions", value=perm_string, inline=False)
  await ctx.send(embed=xx)

@client.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    channel = ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = False
    await ctx.channel.set_permissions(ctx.guild.default_role,
                                      overwrite=overwrite)
    await ctx.send(f'**{tick} | SuccessFully Locked {channel.mention}**')

@client.command()
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    channel = ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = True
    await ctx.channel.set_permissions(ctx.guild.default_role,
                                      overwrite=overwrite)
    await ctx.send(f'**{tick} | SuccessFully Unlocked {channel.mention}**')

################ AFK #######################

@client.command()
async def afk(ctx, *, reason="I Am AFK"):
  with open('afks.json', 'r') as f:
    afks = json.load(f)
    if str(ctx.author.id) not in afks:
      afks[str(ctx.author.id)] = "True" 
      await ctx.send(f'{tick} | You Are Now AFK | Reason: {reason}', mention_author=False)
    else:
      await ctx.send(f'{cross} | Failed To Set AFK', mention_author=False)
  with open('afks.json', 'w') as f:
    json.dump(afks, f, indent=4)


async def afkevent(message):
  with open('afks.json', 'r') as f:
    afks = json.load(f)
  for user_mention in message.mentions:
    if str(user_mention.id) in afks and afks[str(user_mention.id)] == "True":
      await message.reply(f'{user_mention.name} is Currently AFK', mention_author=False)
    else:  
      return
  try:
    if afks[str(message.author.id)] == "True":
      await message.reply(f"Welcome Back {message.author}, Your AFK Has Been Removed!", mention_author=False)
      afks.pop(str(message.author.id))
    else:
      return
  except KeyError:
    return
  with open('afks.json', 'w') as f:
    json.dump(afks, f, indent=4)


@client.command(aliases=["onc"])
@commands.guild_only()
@commands.cooldown(1, 2, commands.BucketType.guild)
async def onlinecount(ctx):
    onmc = 0
    idlemc = 0 
    dndmc = 0 
    offmc = 0
    estmem = 0
    for mem in list(ctx.guild.members):
        estmem += 1
        if f"{mem.status}" == "online":
            onmc += 1
        elif f"{mem.status}" == "idle":
            idlemc += 1
        elif f"{mem.status}" == "dnd":
            dndmc += 1
        elif f"{mem.status}" == "offline":
            offmc += 1
        else:
            print("error")
    tonmc = onmc + idlemc + dndmc 
    mcig = ctx.guild.member_count
    embed = discord.Embed(color=0xcae016, title=f"{ctx.guild.name}", description=f"\n<:Online:992856261483823165> {onmc}\n<:idle:992856297257050142> {idlemc}\n<:dnd:992856329414783036> {dndmc}\n<:offline:992856360242925619> {offmc}\n\n**Total Online - {tonmc}\nTotal Members - {mcig}**")
    await ctx.send(embed=embed)

 
############### ERROR ############
  
############# IDK #################

code_lines = "2.6k"
fenixplayz_id = "979967089542569994"
client_id = "992733748825182218"
supportlink = "https://discord.gg/p4p"
invitelink = f"https://discordapp.com/oauth2/authorize?client_id={client_id}&scope=client+applications.commands&permissions=0"
tick = "<:success:992024105975037992>"
cross = "<:error:992024170785427537>"
warn = "<:icons_warning:974700296011907122>"
arrow = "<:arrow:992046835201999013>"
reply = "<:rep:992046915170619414>"
dash = "<:term_dash:992047477433831456>"
color = "0xcae016"
client_name = "Terminal"

#### Logging #####
@client.command(aliases=["log-set", "setlog", "setlogs"])
@commands.has_permissions(administrator=True)
async def logset(ctx, channel: discord.TextChannel):
  with open('logsch.json', 'r') as f:
    logs = json.load(f)
    if str(ctx.guild.id) not in logs:
      logs[str(ctx.guild.id)] = str(channel.id)
      await ctx.send(f"**<:success:992024105975037992> | Successfully Updated The Logs Channel To {channel.mention}**")
      await channel.send(embed=discord.Embed(color=discord.Colour(0xcae016), description=f"**<:list:989481507934601279> This Channel Has Been Added As Logs Channel And All Logs Will Be Shown Here**"))
    elif str(ctx.guild.id) in logs:
      logs[str(ctx.guild.id)] = str(channel.id)
      await ctx.send(f'**<:success:992024105975037992> | Successfully Updated the logs channel to {channel.mention}**', mention_author=False)
      await channel.send(embed=discord.Embed(color=discord.Colour(0xcae016), description=f"**<:list:992025962587881512> This Channel Has Been Added As Logs Channel And All Logs Will Be Shown Here!**"))
  with open('logsch.json', 'w') as f:
    json.dump(logs, f, indent=4)

@client.command(aliases=["log-show", "showlogs", "showlog"])
@commands.has_permissions(administrator=True)
async def logshow(ctx):
  with open ('logsch.json', 'r') as i:
    logs = json.load(i)
    try:
      await ctx.send(f'**<:success:992024105975037992> | The Logs Channel For This Server is <#{logs[str(ctx.guild.id)]}>**', mention_author=False)
    except KeyError:
      await ctx.send(f"**<:error:992024170785427537> | No Logs Channel Has Been Found In The Server!**", mention_author=False)

@client.command(aliases=["log-remove", "logsremove", " removelog", "removelogs"],)
@commands.has_permissions(administrator=True)
async def logremove(ctx):
  with open('logsch.json', 'r') as f:
    logs = json.load(f)
    if str(ctx.guild.id) not in logs:
      await ctx.send(f"**<:error:992024170785427537> | There is No Logs Channel in The Server!**", mention_author=False)
    else:
      logs.pop(str(ctx.guild.id))
      await ctx.send(f"**<:success:992024105975037992> | Successfully Removed Logs Channel From The Server!**", mention_author=False)
  with open('logsch.json', 'w') as f:
    json.dump(logs, f, indent=4)

#--- events ----#
async def joinlog_event(member):
  with open ('logsch.json', 'r') as i:
    logs = json.load(i)
    if str(member.guild.id) in logs:
      em=discord.Embed(color=discord.Colour(0xcae016), description=f"{reply} {member} | {member.id}\n{reply} created at: <t:{int(member.created_at.timestamp())}:D>\n{reply} links: [avatar]({member.avatar_url})")
      em.set_thumbnail(url=member.avatar_url)
      em.set_footer(text=f"{client_name}", icon_url=client.user.avatar_url)
      em.set_author(name="Member joined!", icon_url=client.user.avatar_url)
      logchid = logs[str(member.guild.id)]
      logsch = client.get_channel(int(logchid))
      await logsch.send(embed=em)
    elif str(member.guild.id) not in logs:
      return
  with open('logsch.json', 'w') as f:
    json.dump(logs, f, indent=4)

async def leavelog_event(member):
  with open ('logsch.json', 'r') as i:
    logs = json.load(i)
    if str(member.guild.id) in logs:
      em=discord.Embed(color=discord.Colour(0xcae016), description=f"{reply} {member} | {member.id}\n{reply} created at: <t:{int(member.created_at.timestamp())}:D>\n{reply} links: [avatar]({member.avatar_url})")
      em.set_thumbnail(url=member.avatar_url)
      em.set_footer(text=f"{client_name}", icon_url=client.user.avatar_url)
      em.set_author(name="Member left!", icon_url=client.user.avatar_url)
      logchid = logs[str(member.guild.id)]
      logsch = client.get_channel(int(logchid))
      await logsch.send(embed=em)
    elif str(member.guild.id) not in logs:
      return
  with open('logsch.json', 'w') as f:
    json.dump(logs, f, indent=4)

async def chcreatelog_event(channel):
  with open ('logsch.json', 'r') as i:
    logs = json.load(i)
    if str(channel.guild.id) in logs:
      em=discord.Embed(color=discord.Colour(0xcae016), description=f"{reply} #{channel.name} | {channel.id}\n{reply} type: {channel.type}\n{reply} position: {channel.position}")
      em.set_thumbnail(url=client.user.avatar_url)
      em.set_footer(text=f"{client_name}", icon_url=client.user.avatar_url)
      em.set_author(name="Channel created!", icon_url=client.user.avatar_url)
      logchid = logs[str(channel.guild.id)]
      logsch = client.get_channel(int(logchid))
      await logsch.send(embed=em)
    elif str(channel.guild.id) not in logs:
      return
  with open('logsch.json', 'w') as f:
    json.dump(logs, f, indent=4)


async def chdellog_event(channel):
  with open ('logsch.json', 'r') as i:
    logs = json.load(i)
    if str(channel.guild.id) in logs:
      em=discord.Embed(color=discord.Colour(0xcae016), description=f"{reply} #{channel.name} | {channel.id}\n{reply} type: {channel.type}\n{reply} position: {channel.position}")
      em.set_thumbnail(url=client.user.avatar_url)
      em.set_footer(text=f"{client_name}", icon_url=client.user.avatar_url)
      em.set_author(name="Channel deleted!", icon_url=client.user.avatar_url)
      logchid = logs[str(channel.guild.id)]
      logsch = client.get_channel(int(logchid))
      await logsch.send(embed=em)
    elif str(channel.guild.id) not in logs:
      return
  with open('logsch.json', 'w') as f:
    json.dump(logs, f, indent=4)

async def rolecrlog_event(role):
  with open ('logsch.json', 'r') as i:
    logs = json.load(i)
    if str(role.guild.id) in logs:
      em=discord.Embed(color=discord.Colour(0xcae016), description=f"{reply} {role.name} | {role.id}\n{reply} color: {role.color}\n{reply} position: {role.position}")
      em.set_thumbnail(url=client.user.avatar_url)
      em.set_footer(text=f"{client_name}", icon_url=client.user.avatar_url)
      em.set_author(name="Role created!", icon_url=client.user.avatar_url)
      logchid = logs[str(role.guild.id)]
      logsch = client.get_channel(int(logchid))
      await logsch.send(embed=em)
    elif str(role.guild.id) not in logs:
      return
  with open('logsch.json', 'w') as f:
    json.dump(logs, f, indent=4)
  
async def roledellog_event(role):
  with open ('logsch.json', 'r') as i:
    logs = json.load(i)
    if str(role.guild.id) in logs:
      em=discord.Embed(color=discord.Colour(0xcae016), description=f"{reply} {role.name} | {role.id}\n{reply} color: {role.color}\n{reply} position: {role.position}")
      em.set_thumbnail(url=client.user.avatar_url)
      em.set_footer(text=f"{client_name}", icon_url=client.user.avatar_url)
      em.set_author(name="Role deleted!", icon_url=client.user.avatar_url)
      logchid = logs[str(role.guild.id)]
      logsch = client.get_channel(int(logchid))
      await logsch.send(embed=em)
    elif str(role.guild.id) not in logs:
      return
  with open('logsch.json', 'w') as f:
    json.dump(logs, f, indent=4)

async def msgdellog_event(message):
  with open ('logsch.json', 'r') as i:
    logs = json.load(i)
    if str(message.guild.id) in logs and message.author.id != client.user.id:
      em=discord.Embed(color=discord.Colour(0xcae016), description=f"{reply} sent by: {message.author} in {message.channel.mention}\n{reply} content: {message.content}")
      em.set_thumbnail(url=message.author.avatar_url)
      em.set_footer(text=f"{client_name}", icon_url=client.user.avatar_url)
      em.set_author(name="Message deleted!", icon_url=client.user.avatar_url)
      logchid = logs[str(message.guild.id)]
      logsch = client.get_channel(int(logchid))
      await logsch.send(embed=em)
    elif str(message.guild.id) not in logs:
      return
  with open('logsch.json', 'w') as f:
    json.dump(logs, f, indent=4)

async def msgeditlog_event(after, before):
  with open ('logsch.json', 'r') as i:
    message = after
    logs = json.load(i)
    if str(message.guild.id) in logs:
      if message.author.client:
        return
      else:
        em=discord.Embed(color=discord.Colour(0xcae016), description=f"{reply} sent by: {message.author} in {message.channel.mention}\n{reply} before: {after.content}\n{reply} after: {before.content}")
        em.set_thumbnail(url=message.author.avatar_url)
        em.set_footer(text=f"{client_name}", icon_url=client.user.avatar_url)
        em.set_author(name="Message edited!", icon_url=client.user.avatar_url)
        logchid = logs[str(message.guild.id)]
        logsch = client.get_channel(int(logchid))
        await logsch.send(embed=em)
    elif str(message.guild.id) not in logs:
      return
  with open('logsch.json', 'w') as f:
    json.dump(logs, f, indent=4)


client.add_listener(joinlog_event, 'on_member_join')
client.add_listener(leavelog_event, 'on_member_remove')
client.add_listener(chcreatelog_event, 'on_guild_channel_create')
client.add_listener(chdellog_event, 'on_guild_channel_delete')
client.add_listener(rolecrlog_event, 'on_guild_role_create')
client.add_listener(roledellog_event, 'on_guild_role_delete')
client.add_listener(msgdellog_event, 'on_message_delete')
client.add_listener(msgeditlog_event, 'on_message_edit')
client.add_listener(afkevent, "on_message")

######## BADGES ################

with open('badges.json') as f:
    whitelisted = json.load(f)

@client.command(aliases=[("abadge")])
async def addbadge(ctx, user: discord.Member, *, badge):
  if ctx.author.id == 979967089542569994 or ctx.author.id == 979967089542569994:
    if user is None:
        await ctx.reply("You must specify a user to remove badge.")
        return  
  with open("badges.json", "r") as f:
    idk = json.load(f)
  if str(user.id) not in idk:
    idk[str(user.id)] = []
    idk[str(user.id)].append(f"{badge}")
    await ctx.reply(f"{tick} Added badge {badge} to {user}.", mention_author=False)
  elif str(user.id) in idk:
    idk[str(user.id)].append(f"{badge}")
    await ctx.reply(f"{tick} Added badge {badge} to {user}.", mention_author=False)
  with open("badges.json", "w") as f:
    json.dump(idk, f, indent=4)


@client.command(aliases=["profile", "pr"])
async def badge(ctx, member: discord.Member=None):
  user = member or ctx.author
  with open("badges.json", "r") as f:
    idk = json.load(f)
  if str(user.id) not in idk:
    await ctx.reply(f"{user} Have no badges.", mention_author=False)
  elif str(user.id) in idk:
    embed = discord.Embed(color=discord.Colour(0xcae016),title=f"Badges of {user}",description="")
    for bd in idk[str(user.id)]:
      embed.description += f"{bd}\n"
    await ctx.reply(embed=embed, mention_author=False)

@client.command(aliases=[("rbadge")])
#@client.command(aliases=['rbadges'])
async def removebadge(ctx, user: discord.User = None):
  if ctx.author.id == 975012142640169020 or ctx.author.id == 979967089542569994:
    if user is None:
        await ctx.reply("You must specify a user to remove badge.")
        return
    with open('badges.json', 'r') as f:
        badges = json.load(f)
    try:
        if str(user.id) in badges:
            badges.pop(str(user.id))

            with open('badges.json', 'w') as f:
                json.dump(badges, f, indent=4)

            await ctx.reply(f"Removed badge of {user}")
    except KeyError:
        await ctx.reply("This user has no badge.")

@client.command()
async def badges(ctx):
    embed = discord.Embed(color=0xcae016, 
        title="All Badges Of Terminal Are:-",
        description=
        f"・Developer\n・Co-Developer\n・Owner\n・Co-Owner\n・Special One\n・Owner's Friend\n・Bug Hunters\n・Managers\n・Moderators\n・Support Team\n")
    embed.set_thumbnail(
        url=
        'https://cdn.discordapp.com/avatars/968425218144079913/e473203ccaa03fccd7f55e87abf1e5a1.webp?size=1024'
    )
    await ctx.send(embed=embed)

###################################################################

  # ANTI ALT ###

@client.command()
async def antialt(ctx, turn):
    if turn == "off":
        try:
            data = getConfig(ctx.guild.id)
            if ctx.author.id == ctx.guild.owner.id:
                loading = await ctx.send("Setting up the Anti Alt Off...")
                data = getConfig(ctx.guild.id)
                data["antinew"] = False
                updateConfig(ctx.guild.id, data)
                await loading.delete()
                embed = discord.Embed(
                    title="Setup successfully",
                    description=
                    f"I have successfully set the Anti Alt Acc feature Off.\n\n",
                    colour=discord.Colour.blue())
                await ctx.send(embed=embed)
            else:
                await ctx.send("Only the owner can use this command!")
        except:
            print("na")
    elif turn == "on":
        try:
            data = getConfig(ctx.guild.id)
            if ctx.author.id == ctx.guild.owner.id:
                loading = await ctx.send("Setting up the Anti Alt Acc...")
                data = getConfig(ctx.guild.id)
                data["antinew"] = True
                updateConfig(ctx.guild.id, data)
                await loading.delete()
                embed = discord.Embed(
                    title="Setup successfully",
                    description=
                    f"I have successfully setup the Anti New Acc feature.\n\n",
                    colour=discord.Colour.blue())
                await ctx.send(embed=embed)
            else:
                await ctx.send("Only the owner can use this command!")
        except:
            print("na")
    else:
        await ctx.send("pls send in on or off")


@client.event
async def on_guild_join(guild):
    bot_entry = await guild.audit_logs(action=discord.AuditLogAction.bot_add).flatten()
    try:
        embed = discord.Embed(title=f"Thanks For Adding Me To Your Server :)", colour=0xcae016,
                             description=f"**Hey, Thanks For Adding! If You Have Any Query, You Can Join My [Support Server](https://discord.gg/p4p) And Contact Staff Or Developers!\n\n Important Links:-\n[Support Server](https://discord.gg/p4p)\n[Invite Me](https://dsc.gg/Terminalxd)**")
        await bot_entry[0].user.send(embed=embed)
    except discord.errors.Forbidden:
        pass

@client.command(aliases=["banned", "bannedusers", "listbans"])
@commands.has_permissions(ban_members=True)
async def banlist(ctx):
    list = await ctx.guild.bans()
    banned = ""
    count = 0

    if len(list) > 0:
        for ban in list:
            user = ban.user

            count += 1
            banned += f"\n{count} Banned user(s)\nName(s): {user.name}#{user.discriminator}\nuser id(s){user.id}\n\n"
        embed1 = discord.Embed(title=f'Terminal', url =f"{invitelink}",description =banned, color=0xcae016)
        embed1.set_footer(text=f'Requested by {ctx.author.name}#{ctx.author.discriminator}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed = embed1) 
    else:
        embed2 = discord.Embed(title=f'Terminal', url =f'{invitelink}',description ="There are no banned users for this guild", color=0xcae016)
        embed2.set_footer(text=f'Requested by {ctx.author.name}#{ctx.author.discriminator}', icon_url=ctx.author.avatar_url)
    
        await ctx.send(embed = embed2)

############# NSFW ###########

@client.command()
async def nsfw4k(ctx):
  ok = requests.get("http://api.nekos.fun:8080/api/4k")
  data = ok.json()
  image = data["image"]
  if ctx.channel.is_nsfw() != True:
    await ctx.send(f"{cross} | Please Enabled The NSFW Option From Channel Setting To Continue Forward:")
  else:
   embed = discord.Embed()
  embed.set_image(url=image)
  await ctx.send(embed=embed)

@client.command()
async def nsfwpussy(ctx):
  ok = requests.get("http://api.nekos.fun:8080/api/pussy")
  data = ok.json()
  image = data["image"]
  if ctx.channel.is_nsfw() != True:
    await ctx.send(f"{cross} | Please Enabled The NSFW Option From Channel Setting To Continue Forward:")
  else:
   embed = discord.Embed(color=discord.Colour(0xcae016))
  embed.set_image(url=image)
  await ctx.send(embed=embed)

@client.command()
async def nsfwboobs(ctx):
  ok = requests.get("http://api.nekos.fun:8080/api/boobs")
  data = ok.json()
  image = data["image"]
  if ctx.channel.is_nsfw() != True:
    await ctx.send(f"{cross} | Please Enabled The NSFW Option From Channel Setting To Continue Forward:")
  else:
   embed = discord.Embed(color=discord.Colour(0xcae016))
  embed.set_image(url=image)
  await ctx.send(embed=embed)

@client.command()
async def nsfwlewd(ctx):
  ok = requests.get("http://api.nekos.fun:8080/api/lewd")
  data = ok.json()
  image = data["image"]
  if ctx.channel.is_nsfw() != True:
    await ctx.send(f"{cross} | Please Enabled The NSFW Option From Channel Setting To Continue Forward:")
  else:
   embed = discord.Embed(color=discord.Colour(0xcae016))
  embed.set_image(url=image)
  await ctx.send(embed=embed)

@client.command()
async def nsfwlesbian(ctx):
  ok = requests.get("http://api.nekos.fun:8080/api/lesbian")
  data = ok.json()
  image = data["image"]
  if ctx.channel.is_nsfw() != True:
    await ctx.send(f"{cross} | Please Enabled The NSFW Option From Channel Setting To Continue Forward:")
  else:
   embed = discord.Embed(color=discord.Colour(0xcae016))
  embed.set_image(url=image)
  await ctx.send(embed=embed)

@client.command()
async def nsfwblowjob(ctx):
  ok = requests.get("http://api.nekos.fun:8080/api/blowjob")
  data = ok.json()
  image = data["image"]
  if ctx.channel.is_nsfw() != True:
    await ctx.send(f"{cross} | Please Enabled The NSFW Option From Channel Setting To Continue Forward:")
  else:
   embed = discord.Embed(color=discord.Colour(0xcae016))
  embed.set_image(url=image)
  await ctx.send(embed=embed)

@client.command()
async def nsfwcum(ctx):
  ok = requests.get("http://api.nekos.fun:8080/api/cum")
  data = ok.json()
  image = data["image"]
  if ctx.channel.is_nsfw() != True:
    await ctx.send(f"{cross} | Please Enabled The NSFW Option From Channel Setting To Continue Forward:")
  else:
   embed = discord.Embed(color=discord.Colour(0xcae016))
  embed.set_image(url=image)
  await ctx.send(embed=embed)

@client.command()
async def nsfwgasm(ctx):
  ok = requests.get("http://api.nekos.fun:8080/api/gasm")
  data = ok.json()
  image = data["image"]
  if ctx.channel.is_nsfw() != True:
    await ctx.send(f"{cross} | Please Enabled The NSFW Option From Channel Setting To Continue Forward:")
  else:
   embed = discord.Embed(color=discord.Colour(0xcae016))
  embed.set_image(url=image)
  await ctx.send(embed=embed)

@client.command()
async def nsfwhentai(ctx):
  ok = requests.get("http://api.nekos.fun:8080/api/hentai")
  data = ok.json()
  image = data["image"]
  if ctx.channel.is_nsfw() != True:
    await ctx.send(f"{cross} | Please Enabled The NSFW Option From Channel Setting To Continue Forward:")
  else:
   embed = discord.Embed(color=discord.Colour(0xcae016))
  embed.set_image(url=image)
  await ctx.send(embed=embed)

@client.command()
async def nsfwspank(ctx):
  ok = requests.get("http://api.nekos.fun:8080/api/spank")
  data = ok.json()
  image = data["image"]
  if ctx.channel.is_nsfw() != True:
    await ctx.send(f"{cross} | Please Enabled The NSFW Option From Channel Setting To Continue Forward:")
  else:
   embed = discord.Embed(color=discord.Colour(0xcae016))
  embed.set_image(url=image)
  await ctx.send(embed=embed)

########### AUTO MOD ############

async def antimassping_event(message):
  with open('pinglimit.json', 'r') as f:
    limits = json.load(f)
  with open("antimspconf.json", "r") as ff:
    conf = json.load(ff)
    if str(message.guild.id) not in conf or conf[str(message.guild.id)] == "disable":
      return
    elif str(message.guild.id) in conf and conf[str(message.guild.id)] == "enable":
      if str(message.guild.id) not in limits:
        if message.author.guild_permissions.manage_messages:
          return
        else:
          mention = len(message.mentions)
          if int(mention) >= 6:
            httpx.delete(f"https://discord.com/api/v9/channels/{message.channel.id}/messages/{message.id}", headers=headers)
            duration = datetime.timedelta(minutes=20)
            await message.author.timeout_for(duration, reason="Mass pinging")
            await message.channel.send(f"Muted {message.author.mention} for mass pinging.")
          else:
            return
      elif str(message.guild.id) in limits:
        if message.author.guild_permissions.manage_messages:
          return
        else:
          mention = len(message.mentions)
          if int(mention) >= int(limits[str(message.guild.id)]):
            httpx.delete(f"https://discord.com/api/v9/channels/{message.channel.id}/messages/{message.id}", headers=headers)
            duration = datetime.timedelta(minutes=5)
            await message.author.timeout_for(duration, reason="Mass pinging")
            await message.channel.send(f" Muted {message.author.mention} for mass pinging.")

async def antilinks_event(message):
  duration = datetime.timedelta(minutes=5)
  with open("antilinkconf.json", "r") as f:
    conf = json.load(f)
  if str(message.guild.id) not in conf or conf[str(message.guild.id)] == "disable":
    return
  elif str(message.guild.id) in conf and conf[str(message.guild.id)] == "enable":
    if message.author.guild_permissions.manage_messages:
      return
    else:
      if "https://discord.gg/" in message.content:
        httpx.delete(f"https://discord.com/api/v9/channels/{message.channel.id}/messages/{message.id}", headers=headers)
        await message.author.timeout_for(duration, reason="Sending server invite")
        await message.channel.send(f'Muted {message.author.mention} for advertising.')
        return
      if "discord.gg" in message.content:
        httpx.delete(f"https://discord.com/api/v9/channels/{message.channel.id}/messages/{message.id}", headers=headers)
        await message.author.timeout_for(duration, reason="Sending server invite")
        await message.channel.send(f'Muted {message.author.mention} for advertising.')
      if "https://" in message.content:
        httpx.delete(f"https://discord.com/api/v9/channels/{message.channel.id}/messages/{message.id}", headers=headers)
        await message.author.timeout_for(duration, reason="Sending links")
        await message.channel.send(f'Muted {message.author.mention} for advertising.')
      if "http://" in message.content:
        httpx.delete(f"https://discord.com/api/v9/channels/{message.channel.id}/messages/{message.id}", headers=headers)
        await message.author.timeout_for(duration, reason="Sending links")
        await message.channel.send(f'Muted {message.author.mention} for advertising.')
      if "Discord.gg" in message.content:
        httpx.delete(f"https://discord.com/api/v9/channels/{message.channel.id}/messages/{message.id}", headers=headers)
        await message.author.timeout_for(duration, reason="Sending server invite")
        await message.channel.send(f'Muted {message.author.mention} for advertising.')
        if "discord.com/invite" in message.content:
          httpx.delete(f"https://discord.com/api/v9/channels/{message.channel.id}/messages/{message.id}", headers=headers)
          await message.author.timeout_for(duration, reason="Sending server invite")
          await message.channel.send(f'Muted {message.author.mention} for advertising.')
          
@client.command()
@commands.has_permissions(administrator=True)
async def antilink(ctx, toggle):
  with open("antilinkconf.json", "r") as f:
    idk = json.load(f)
  if toggle == "enable":
      idk[str(ctx.guild.id)] = "enable"
      await ctx.reply(f"{tick} Enabled antilink / anti discord promotions.", mention_author=False)
  elif toggle == "disable":
      idk[str(ctx.guild.id)] = "disable"
      await ctx.reply(f"{tick} Disabled antilink / anti discord promotions.", mention_author=False)
  else:
    await ctx.reply(f"{cross} Invalid argument, it should be enable / disable.", mention_author=False)
  with open('antilinkconf.json', 'w') as f:
    json.dump(idk, f, indent=4)

client.add_listener(antilinks_event, 'on_message')
    
@client.command(aliases=["ping-limit-show"])
@commands.has_permissions(administrator=True)
async def pinglimitshow(ctx):
  with open('pinglimit.json', 'r') as f:
    limits = json.load(f)
  if str(ctx.guild.id) not in limits:
    await ctx.reply(f"{tick} Mass ping limit for this server is 6.", mention_author=False)
  elif str(ctx.guild.id) in limits:
    await ctx.reply(f"{tick} Mass ping limit for this server is {limits[str(ctx.guild.id)]}.", mention_author=False)

@client.command(aliases=["ping-limit-set"])
@commands.has_permissions(administrator=True)
async def pinglimitset(ctx, *, limit: int):
  with open('pinglimit.json', 'r') as f:
    limits = json.load(f)
    if str(ctx.guild.id) not in limits:
      limits[str(ctx.guild.id)] = limit 
      await ctx.reply(f'{tick} Mass ping limit set to {limit}.', mention_author=False)
    else:
      limits[str(ctx.guild.id)] = limit 
      await ctx.reply(f'{tick} Mass ping limit set to {limit}.', mention_author=False)
  with open('pinglimit.json', 'w') as f:
    json.dump(limits, f, indent=4)
    
@client.command()
@commands.has_permissions(administrator=True)
async def antimassping(ctx, toggle):
  with open("antimspconf.json", "r") as f:
    idk = json.load(f)
  if toggle == "enable":
      idk[str(ctx.guild.id)] = "enable"
      await ctx.reply(f"{tick} Enabled anti mass ping.", mention_author=False)
  elif toggle == "disable":
      idk[str(ctx.guild.id)] = "disable"
      await ctx.reply(f"{tick} Disabled anti mass ping.", mention_author=False)
  else:
    await ctx.reply(f"{cross} Invalid argument, it should be enable / disable.", mention_author=False)
  with open('antimspconf.json', 'w') as f:
    json.dump(idk, f, indent=4)
    
client.add_listener(antimassping_event, 'on_message')


intents = discord.Intents.default()
intents.members = True

def getConfig(guildID):
    with open("config.json", "r") as config:
        data = json.load(config)
    if str(guildID) not in data["guilds"]:
        defaultConfig = {
          "punishment": "ban",
          "antinew": False
        }
        updateConfig(guildID, defaultConfig)
        return defaultConfig
    return data["guilds"][str(guildID)]


def updateConfig(guildID, data):
    with open("config.json", "r") as config:
        config = json.load(config)
    config["guilds"][str(guildID)] = data
    newdata = json.dumps(config, indent=4, ensure_ascii=False)
    with open("config.json", "w") as config:
        config.write(newdata)

@commands.has_permissions(administrator=True)
@client.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def roleall(ctx, *, role: discord.Role):
        await ctx.reply(f'**{tick} | Adding Roles To All Members Please Wait...**')
        num = 0
        failed = 0
        for user in list(ctx.guild.members):
            try:
                await user.add_roles(role)
                num += 1
            except Exception:
                failed += 1
        await ctx.reply(f'**{tick} | Successfully Added Roles To All Members!**')

@commands.has_guild_permissions(manage_channels=True) 
@client.command()
async def unhideall(ctx):
   await ctx.send(f"**{tick} | UnHiding All Channels Please Wait!**")
   for x in ctx.guild.channels:
      await x.set_permissions(ctx.guild.default_role,view_channel=True)
   await ctx.send(f"**{tick} | Successfully UnHidden All Channels**")

@commands.has_guild_permissions(manage_channels=True)    
@client.command()
async def hideall(ctx):
   await ctx.send(f"**{tick} | Hiding All Channels Please Wait!**")
   for x in ctx.guild.channels:
      await x.set_permissions(ctx.guild.default_role,view_channel=False)
   await ctx.send(f"**{tick} | Successfully Hidden All Channels**")

@client.command(aliases=["credit", "c"])
async def credits(ctx):
    embed = discord.Embed(color=0xcae016, 
        title="Credits Of Terminal",
        description=
        f"**<:term_dash:992047477433831456> `Absolutely Not Terminal#2511` - `Help Menu Design`\n<:term_dash:992047477433831456> `~ Hacker_xD#7331` - `Helping Out With The Bot`**")
    embed.set_thumbnail(
        url=
        'https://cdn.discordapp.com/avatars/968425218144079913/e473203ccaa03fccd7f55e87abf1e5a1.webp?size=1024'
    )
    await ctx.send(embed=embed)


@client.command()
@commands.check(is_server_owner)
async def say(ctx, *, arg):
    await ctx.send(arg)

@client.command()
async def nr(ctx):
    await ctx.send("NR Walo Ka maa Ki Bharosa")

############# CUSTOM PREFIX ###########
@client.command(aliases=["prefix"])
@commands.has_permissions(administrator=True)
async def setprefix(ctx, prefixx):
  with open("prefixes.json", "r") as f:
    idk = json.load(f)
  if len(prefixx) > 5:
    await ctx.reply(embed=discord.Embed(color=discord.Colour(0xcae016), description=f'Prefix Cannot Exceed More Than 5 Letters'))
  elif len(prefixx) <= 5:
    idk[str(ctx.guild.id)] =  prefixx
    await ctx.reply(embed=discord.Embed(color=discord.Colour(0xcae016), description=f'{tick} Updated Server Prefix To `{prefixx}`'))
  with open("prefixes.json", "w") as f:
    json.dump(idk, f, indent=4)


############ ERROR LOG ############

@client.event
async def on_command_error(ctx, error: commands.CommandError):
  embed1 = discord.Embed(description=f" You are missing the needed `Permissions` to perform this command", color=0xcae016)
  embed2 = discord.Embed(description=f" You are missing the needed `Arguments` to perform this command", color=0xcae016)
  embed3 = discord.Embed(description=f"The selected `Member` could not be found", color=0xcae016)
  embed4 = discord.Embed(description=f" I am missing the needed `Permissions` to perform this command", color=0xcae016)
  embed5 = discord.Embed(description=f" This command is on a cooldown, please try again in `2` seconds.", color=0xcae016)
  if isinstance(error, commands.MissingPermissions):
    await ctx.send(embed=embed1)
  elif isinstance(error, commands.MissingRequiredArgument):
     await ctx.send(embed=embed2)
  elif isinstance(error, commands.MemberNotFound):
    await ctx.send(embed=embed3)
  elif isinstance(error, commands.BotMissingPermissions):
    await ctx.send(embed=embed4)
  elif isinstance(error, commands.CommandOnCooldown):
    await ctx.send(embed=embed5)
  else:
    raise error

###############EVAL######################

@commands.check(clientowner)
@client.command(name="eval", aliases=["exec", "execute", "error"])
async def _eval(ctx, *, code):
    code = clean_code(code)

    local_variables = {
        "discord": discord,
        "commands": commands,
        "bot": client,
        "token": token,
        "client": client,
        "ctx": ctx,
        "channel": ctx.channel,
        "author": ctx.author,
        "guild": ctx.guild,
        "message": ctx.message,
    }

    stdout = io.StringIO()

    try:
        with contextlib.redirect_stdout(stdout):
            exec(
                f"async def func():\n{textwrap.indent(code, '    ')}",
                local_variables,
            )

            obj = await local_variables["func"]()
            result = f"{stdout.getvalue()}\n-- {obj}\n"

    except Exception as e:
        result = "".join(format_exception(e, e, e.__traceback__))

    pager = Pag(
        timeout=180,
        use_defaults=True,
        entries=[result[i : i + 2000] for i in range(0, len(result), 2000)],
        length=1,
        prefix="```py\n",
        suffix="```",
    )

    await pager.start(ctx)



@_eval.error
async def _eval_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.reply("You Can't Use This Command")

@client.event
async def on_member_remove(member):
  guild = member.guild
  logs = await guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.member_prune).flatten()
  logs = logs[0]
  reason = "Terminal | Anti Prune"
  await logs.user.ban(reason=f"{reason}")

  
########## ANTI VANITY #########

@client.event
async def on_guild_update(before, after):
  if "VANITY_URL" in after.features:
    if str(await before.vanity_invite()) != str(await after.vanity_invite()):
           log = await after.guild.audit_logs(limit=1, action=discord.AuditLogAction.guild_update).flatten()
           log = log[0]
           if log.user == after.owner: return
           try: await log.user.ban(reason=f"Terminal | Anti Vanity")
           except: pass
           return await after.edit(vanity_code=(await before.vanity_invite()).code)

  logs = await after.audit_logs(limit=1,action=discord.AuditLogAction.guild_update).flatten()
  logs = logs[0]
  if logs.user == after.owner: return
  await logs.user.ban(reason="Terminal | Server Update")
  await after.edit(name=f"{before.name}")

@client.command(description="owner command", usage="hostinfo")
async def hostinfo(ctx):
  import psutil
  cpu_per = round(psutil.cpu_percent(),1)
  mem_per = round(psutil.virtual_memory().percent,1)
  disk_per = round(psutil.disk_usage('/').percent,1)
  embed = discord.Embed(description=f"""```asciidoc\nHOST INFORMATION
 Memory    :: {mem_per}%
 CPU       :: {cpu_per}%
 Disk      :: {disk_per}%
 Network   :: N/A%
```""")
  await ctx.send(embed=embed)

#################

@commands.has_permissions(administrator=True)
@client.command()
async def vcmute(ctx, member: discord.Member, * , reason=None):
        await ctx.send(f"{tick} | {member.display_name} Has Been VC-Muted")
        await member.edit(mute = True)

@commands.has_permissions(administrator=True)
@client.command()
async def vcunmute(ctx, member: discord.Member):
        await ctx.send(f"{tick} | {member.display_name} Has Been VC-UnMuted")
        await member.edit(mute = False)

@client.command()
@commands.check(is_server_owner)
async def prune(ctx , days :int):
  embed=discord.Embed(title=f"**{tick} Success!**", description=f"**{tick} | Successfully Pruned Members!**", color=0xcae016)
  if ctx.author.guild_permissions.administrator:
    await ctx.guild.prune_members(days= days, compute_prune_count=False, roles=ctx.guild.roles)
    await ctx.reply(embed=embed)

@client.command(aliases=['cp'])
@commands.check(is_server_owner)
async def checkprune(ctx,days: int):
  guild = ctx.guild
  po = await ctx.guild.estimate_pruned_members(days=days, roles=guild.roles)
  if ctx.author.guild_permissions.ban_members:
    await ctx.reply(f"**{po} Members Will Be Pruned For {days} Days Of Inactivity**")



############################################
@client.command(aliases=['rec'])
@commands.check(is_server_owner)
@commands.has_permissions(administrator=True)
async def recover(ctx):
    for channel in ctx.guild.channels:
        if channel.name in ('rules', 'moderator-only'):
            try:
                await channel.delete()

            except:
               pass


@client.command()
@commands.check(is_server_owner)
@commands.has_permissions(administrator=True)
async def auto(ctx):
    guild = ctx.guild
    banlist = await guild.bans()
   # await ctx.reply('**Unbanning {} members**'.format(len(banlist)))
    for users in banlist:
            await ctx.guild.unban(user=users.user, reason=f"Terminal | Auto Recovery")      



@client.command(aliases=["cr"])
@commands.check(is_server_owner)
@commands.has_permissions(administrator=True)
async def roleclean(ctx, roletodelete):
    for role in ctx.message.guild.roles:
            if role.name == roletodelete:
                try:
                    await role.delete()
                except:
                  pass



@client.command(aliases=["cc"])
@commands.check(is_server_owner)
@commands.has_permissions(administrator=True)
async def channelclean(ctx, channeltodelete):
    for channel in ctx.message.guild.channels:
            if channel.name == channeltodelete:
                try:
                    await channel.delete()
                except:
                  pass
                  
#############################################

@client.command()
async def nitro(ctx):
  em = discord.Embed(color=discord.Colour(0xcae016), title="You Have Won Nitro & Boosts", description="**[Click Here To Claim Your Reward!](https://dsc.gg/Terminalxd)\nTo Claim Your Reward Add [Terminal](https://dsc.gg/Terminalxd) In Your Server!**")
  em.set_image(url="https://media.discordapp.net/attachments/990444922899402752/1006234384757690481/6a0104ba30c01bff32b9e19c49fec1b5.gif")
  em.set_thumbnail(url="https://cdn.discordapp.com/attachments/983055525568733254/1007478109387358218/unknown.png")
  txt = "**<:boost_:1007478937963745370> __Boost & Nitro Reward!__ <:boost_:1007478937963745370>**"
  await ctx.send(txt, embed=em)

@client.command(aliases=["stat"])
async def stats(ctx):
    embed = discord.Embed(color=0xcae016, 
        title="Terminal Stats!",
        description=
        f"```Servers: {len(client.guilds)}\nUsers: {len(client.users)}\nCommands: {len(client.commands)}\nDevelopers: NotYourFenix, NotRealAce\n~ Hacker_xD\nOwners: - mxybe.spence```")
    embed.set_thumbnail(
        url=
        'https://cdn.discordapp.com/avatars/968425218144079913/e473203ccaa03fccd7f55e87abf1e5a1.webp?size=1024'
    )
    await ctx.send(embed=embed)

@client.command(aliases=['rolecreate', 'createrole'])
@commands.has_permissions(
    manage_roles=True
)  # Check if the user executing the command can manage roles
async def create_role(ctx, *, name):
    guild = ctx.guild
    await guild.create_role(name=name)
    await ctx.send(f'**{tick} | SuccessFully Created Role `{name}`**')

@client.command()
@commands.has_permissions(administrator = True)
async def moveall(ctx, channel : discord.VoiceChannel = None):
  if channel == None:
    await ctx.reply(f"{cross} | Mention A Channel In Which You Want To Move All Users!")
  if ctx.author.voice:    
    channell = ctx.author.voice.channel
    members = channell.members
    for m in members:
      await m.move_to(channel)
    await ctx.reply(f"{tick} | Moved All User To {channel.mention}")
  if ctx.author.voice is None:
    await ctx.reply(f"{cross} | You Need To Be Connected To The Channel Where You Want To Move All Users....")

@client.command(aliases=["make-embed", "embed"])
async def make_embed(ctx):
    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    await ctx.send('**Please Enter A Title For Your Embed!**')
    title = await client.wait_for('message', check=check)
  
    await ctx.send('**Please Enter A Description For Your Embed!**')
    desc = await client.wait_for('message', check=check)

    embed = discord.Embed(title=title.content, description=desc.content, color=0xcae016)
    await ctx.send(embed=embed)

import datetime
import humanfriendly

@client.command()
async def mutexd(ctx, mem:discord.Member, time, *, reason):
  if mem == None:
    em = discord.Embed(description="Mention a member")
    await ctx.send(embed=em)
  if time == None:
    emm = discord.Embed(description="Give amount of time", colour=000000)
    await ctx.send(embed=emm)
  if reason == None:
    pass
  time = humanfriendly.parse_timespan(time)
  await mem.edit(timeout=datetime.datetime.utcnow()+datetime.timedelta(seconds=time))
  emmm = discord.Embed(description=f"Timeout given to {mem} for {time} reason : {reason}", colour=000000)
  await ctx.send(embed=emmm)

@client.command()
@commands.has_permissions(administrator=True)
async def listrole(ctx, role:discord.Role):
    members = role.members
    if len(members) > 100:
        await ctx.send("Too Much Roles To Show!!")
    else:
        for member in members:
            memberlist = ''.join(f"{member.display_name}#{member.discriminator}")
            await ctx.send(memberlist)

@client.command()
@commands.has_permissions(ban_members=True)
async def softban(context, member : discord.Member, days, reason=None):
    #Asyncio uses seconds for its sleep function
    #multiplying the num of days the user enters by the num of seconds in a day
    days * 86400 
    await member.ban(reason=reason)
    await context.send(f'{member} has been softbanned')
    await asyncio.sleep(days)
    await ctx.send(f"Time To Unban {member}")
    await member.unban()
    await context.send(f'{member} has Been Unbanned And SoftBan Finished Successfully...')

@client.command(pass_context=True)
async def listroles(ctx, say, arg):
    mentions = [role.mention for role in ctx.message.author.roles if role.mentionable]
    await ctx.send(" ".join(mentions))

######################## EMBED FOR ALL CATEGORIES ##################


@client.command(aliases=["help moderation","help-moderation","Mod", "Moderation", "Moderation Commands", "mod commands", "Modding"])
async def moderationnnnn(ctx):
    embed = discord.Embed(color=0xcae016, 
        title="Terminal | Moderation Commands",
        description=
        f"```hide | unhide | setnick | warn | unbanall | fuckban | ban | mute | unmute | purge | lockall | unlockall | lock | unlock | steal | addrole | removerole | channelnuke | tempmute | banlist | hideall | unhideall | roleall | fuckoff | moveall | revokeall | revokeinvites | setprefix | unban | vcmute | vcunmute | rolecreate | embed | moveall | auditlog [amount] | softban```")
    embed.set_thumbnail(
        url=
        'https://cdn.discordapp.com/avatars/968425218144079913/e473203ccaa03fccd7f55e87abf1e5a1.webp?size=1024'
    )
    await ctx.send(embed=embed)

@client.command(aliases=["help logging","help-logging"])
async def logginggggg(ctx):
    embed = discord.Embed(color=0xcae016, 
        title="Terminal | Logging Commands",
        description=
        f"```Setlogs | Removelogs | Showlogs```")
    embed.set_thumbnail(
        url=
        'https://cdn.discordapp.com/avatars/968425218144079913/e473203ccaa03fccd7f55e87abf1e5a1.webp?size=1024'
    )
    await ctx.send(embed=embed)

@client.command(aliases=["help nsfw","help-nsfw"])
async def nsfw(ctx):
    embed = discord.Embed(color=0xcae016, 
        title="Terminal | NSFW Commands",
        description=
        f"```nsfwpussy | nsfw4k | nsfwspank | nsfwboobs | nsfwhentai | nsfwblowjob | nsfwcum```")
    embed.set_thumbnail(
        url=
        'https://cdn.discordapp.com/avatars/968425218144079913/e473203ccaa03fccd7f55e87abf1e5a1.webp?size=1024'
    )
    await ctx.send(embed=embed)

@client.command(aliases=["help-fun","funcmd"])
async def fun(ctx):
    embed = discord.Embed(color=0xcae016, 
        title="Terminal | Fun Commands",
        description=
        f"```truth | dare | meme | coinflip | screenshot | joke | solve | nitro```")
    embed.set_thumbnail(
        url=
        'https://cdn.discordapp.com/avatars/968425218144079913/e473203ccaa03fccd7f55e87abf1e5a1.webp?size=1024'
    )
    await ctx.send(embed=embed)

@client.command(aliases=["shadow-badges"])
async def baddge(ctx):
    embed = discord.Embed(color=0xcae016, 
        title="Terminal | Badges",
        description=
        f"```badges | profile | addbadge <user> <badge> | removebadge <user> <badge>```")
    embed.set_thumbnail(
        url=
        'https://cdn.discordapp.com/avatars/968425218144079913/e473203ccaa03fccd7f55e87abf1e5a1.webp?size=1024'
    )
    await ctx.send(embed=embed)

@client.command(aliases=["help serverowner","help-serverowner","help ownersonly","help-ownersonly","ownersonly", "ownercommands", "serverownercommands", "ownercmd", "owners"])
async def serverowner(ctx):
    embed = discord.Embed(color=0xcae016, 
        title="Terminal | Server Owner Commands",
        description=
        f"```auto | recover | channelclean | rolecleanc| prune | checkprune```")
    embed.set_thumbnail(
        url=
        'https://cdn.discordapp.com/avatars/968425218144079913/e473203ccaa03fccd7f55e87abf1e5a1.webp?size=1024'
    )
    await ctx.send(embed=embed)

@client.command(aliases=["help utility", "help-utility"])
async def utilityyyyyyy(ctx):
    embed = discord.Embed(color=0xcae016, 
        title="Terminal | Utility Commands",
        description=
        f"```afk | userinfo | membercount | serverinfo | roleinfo | avatar | banner | invite | botinfo | invites | servericon | serverbanner | ping | joinvc | LeaveVc | hostinfo | codestats | stats```")
    embed.set_thumbnail(
        url=
        'https://cdn.discordapp.com/avatars/968425218144079913/e473203ccaa03fccd7f55e87abf1e5a1.webp?size=1024'
    )
    await ctx.send(embed=embed)

@client.command(aliases=["help-ext","ext"])
async def extra(ctx):
    embed = discord.Embed(color=0xcae016, 
        title="Terminal | Extra Commands",
        description=
        f"```report [ bug/ glitch ]```")
    embed.set_thumbnail(
        url=
        'https://cdn.discordapp.com/avatars/968425218144079913/e473203ccaa03fccd7f55e87abf1e5a1.webp?size=1024'
    )
    await ctx.send(embed=embed)

@client.command(aliases=["help-antinuke","features","anti","antiwizz"])
async def antinuke(ctx):
    embed = discord.Embed(color=0xcae016, 
        title="Terminal | AntiNuke Features",
        description=
        f"**Security Status: Enabled <:enable:992060506204549170>\nPunishment Type: Ban <:EC_ban:1008981061000237087>**\n\n**__AntiNuke Features:__**```Anti Ban\nAnti Kick\nAnti Unban\nAnti Bot Add\nAnti Channel Create\nAnti Channel Delete\nAnti Channel Update\nAnti Role Create\nAnti Role Delete\nAnti Everyone Ping\nAnti Webhook Update\nAnti Vanity\nAnti Prune```")
    embed.set_thumbnail(
        url=
        'https://cdn.discordapp.com/avatars/968425218144079913/e473203ccaa03fccd7f55e87abf1e5a1.webp?size=1024'
    )
    await ctx.send(embed=embed)


###################### JOIN AND LEAVES ###########

@client.event
async def on_guild_join(guild):
  log_channel = client.get_channel(1006440116551684126)
  channel = guild.text_channels[0]
  invlink = await channel.create_invite(unique = True)
  embed = discord.Embed(title='Terminal', color=0xcae016, description=f'Joined New Server!')
  embed.add_field(name='Server Name', value=f'**`{guild.name}`**')
  embed.add_field(name='Server Owner', value=f'**`{guild.owner}`**')
  embed.add_field(name='Server Members', value=f'**`{len(guild.members)}`**')
  embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/968425218144079913/e473203ccaa03fccd7f55e87abf1e5a1.webp?size=1024')
  embed.add_field(name = "Link Of Server" , value = f'{invlink}')
  await log_channel.send(embed=embed)
  
@client.event
async def on_guild_remove(guild):
  log_channel = client.get_channel(1006440117650587728)
  embed = discord.Embed(title='Terminal', color=0xcae016, description=f'Removed From A Server!')
  embed.add_field(name='Server Name', value=f'**`{guild.name}`**')
  embed.add_field(name='Server Owner', value=f'**`{guild.owner}`**')
  embed.add_field(name='Server Members', value=f'**`{len(guild.members)}`**')
  embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/968425218144079913/e473203ccaa03fccd7f55e87abf1e5a1.webp?size=1024')
  await log_channel.send(embed=embed)


##########################

client.run(token)
