import discord
import datetime
import os
import random
import asyncio
import contextlib
import json
from discord_components import *
from discord.ext import commands

client = discord.Client

update = "`All bug fixed`"

publicembed = discord.Embed(title="Terminal | Public Commands", description="""
`You Can Also Use a?help-utility`\n```afk | userinfo | membercount | serverinfo | roleinfo | avatar | banner | invite | botinfo | invites | servericon | serverbanner | ping | joinvc | LeaveVc | hostinfo | codestats | stats```
""", color=0x2f3136)
publicembed.set_footer(text="Made With 🧠 By NotYourFenix#5465")

adminembed = discord.Embed(title="Terminal | Moderation Commands", description="""
`You Can Also Use a?help-moderation`\n```hide | unhide | setnick | warn | unbanall | fuckban | ban | mute | unmute | purge | lockall | unlockall | lock | unlock | steal | addrole | removerole | channelnuke | tempmute | banlist | hideall | unhideall | roleall | fuckoff | moveall | revokeall | revokeinvites | setprefix | unban | vcmute | vcunmute | rolecreate | embed | moveall | auditlog [amount] | softban```
""", color=0x2f3136)
adminembed.set_footer(text="Made With 🧠 By NotYourFenix#5465")

badgeembed = discord.Embed(title="Terminal | Badge Commands",description="""
`You Can Also Use a?help-showbadges`\n```badges | profile | addbadge <user> <badge> | removebadge <user> <badge>```
""", color=0x2f3136)
badgeembed.set_footer(text="Made With 🧠 By NotYourFenix#5465")


logembed = discord.Embed(title="Terminal | Logging Commands",description="""
`You Can Also Use a?help-logging`\n```Setlogs | Removelogs | Showlogs```
""", color=0x2f3136)
logembed.set_footer(text="Made With 🧠 By NotYourFenix#5465")


nsfwembed = discord.Embed(title="Terminal | NSFW Commands",description="""
`You Can Also Use a?help-nsfw`\n```nsfwpussy | nsfw4k | nsfwspank | nsfwboobs | nsfwhentai | nsfwblowjob | nsfwcum```
""", color=0x2f3136)
nsfwembed.set_footer(text="Made With 🧠 By NotYourFenix#5465")


gamesembed = discord.Embed(title="Terminal | Fun Commands",description="""
`You Can Also Use a?help-fun`\n```truth | dare | meme | coinflip | screenshot | joke | solve | nitro```
""", color=0x2f3136)
gamesembed.set_footer(text="Made With 🧠 By NotYourFenix#5465")


antinukeembed = discord.Embed(title="Terminal | AntiNuke Features",description="""__Security Status__\nEnabled""", color=0x2f3136)
antinukeembed.add_field(name="__Punishment Type__",
                         value=f"Ban",
                         inline=False)
antinukeembed.add_field(name="Features", value="```Anti Ban\nAnti Kick\nAnti Unban\nAnti Bot Add\nAnti Channel Create\nAnti Channel Delete\nAnti Channel Update\nAnti Role Create\nAnti Role Delete\nAnti Everyone Ping\nAnti Webhook Update\nAnti Vanity\nAnti Prune```\n`You Can Also Use a?help-antinuke`")
antinukeembed.set_footer(text="Made With 🧠 By NotYourFenix#5465")


extraembed = discord.Embed(title="Terminal | Extra Commands",description="""
`You Can Also Use a?help-ext`\n```report [ bug/ glitch ]```
""", color=0x2f3136)
extraembed.set_footer(text="Made With 🧠 By NotYourFenix#5465")

ownerembed = discord.Embed(title="Terminal | Server Owner Commands",description="""
`You Can Also Use a?help-serverowner`\n```auto | recover | channelclean | rolecleanc| prune | checkprune```
""", color=0x2f3136)
ownerembed.set_footer(text="Made With 🧠 By NotYourFenix#5465")

class help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @commands.command(aliases=["h"])
    @commands.bot_has_permissions(embed_links=True)
    async def help(self, ctx):
      await self.selectboxtesting(ctx)
    

  
    async def selectboxtesting(self, ctx):
      publicemoji = self.bot.get_emoji(1005816928062935111)
      adminemoji = self.bot.get_emoji(1006464545411317800)
      logemoji = self.bot.get_emoji(992025962587881512)
      funemoji = self.bot.get_emoji(1001173447868694568)
      antinukeemoji = self.bot.get_emoji(1001173459952468059)
      extraemoji = self.bot.get_emoji(1001173411432775770)
      badgeemoji = self.bot.get_emoji(1001172244707426435)
      nsfwemoji = self.bot.get_emoji(1006465026804174918)
      owneremoji = self.bot.get_emoji(1000814308239888455)
      embed = discord.Embed(title="Terminal Help Menu", description=f"""**HELLO SKID WLCOME**""", color=0xcae016)
      embed.set_thumbnail(url=self.bot.user.avatar_url)
      embed.set_footer(text="Made With 🧠 By NotYourFenix#5465",icon_url= "https://cdn.discordapp.com/avatars/968425218144079913/63b021f7d084709ed06406237d3dff4a.webp?size=1024")
      interaction1 = await ctx.send(embed=embed,
        components=[[
            Select(
                placeholder="Select Category",
                options=[
                    SelectOption(
                        label="Utilty Commands",
                        value="1", emoji=publicemoji),
                    SelectOption(
                        label="Moderator Commands",
                        value="2", emoji=adminemoji),
                    SelectOption(
                        label="Logging Commands",
                        value="3", emoji=logemoji),
                    SelectOption(
                        label="Fun Commands",
                        value="4", emoji=funemoji), 
                    SelectOption(
                        label="AntiNuke Features",
                        value="5", emoji=antinukeemoji),
                    SelectOption(
                ],
                custom_id="selectboxtesting")
        ]])
      while True:
        try:
            interaction2 = await self.bot.wait_for("select_option",check=lambda inter: inter.custom_id == "selectboxtesting", timeout=1800)
            res = interaction2.values[0]
            if res == "1":
                await interaction2.send(embed=publicembed)
            elif res == "2":
                await interaction2.send(embed=adminembed)
            elif res == "3":
                await interaction2.send(embed=logembed)
            elif res == "4":
                await interaction2.send(embed=gamesembed)
            elif res == "5":
                await interaction2.send(embed=antinukeembed)
            elif res == "6":
              await interaction2.send(embed=extraembed)
            else:
              pass
        except discord.errors.HTTPException:
          error = "sex"
          print(error)


def setup(bot):
    bot.add_cog(help(bot))
