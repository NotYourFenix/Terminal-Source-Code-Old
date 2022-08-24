import os
import discord
import datetime
from discord.ext import commands, tasks
#import httpx


IGNORE = [975012142640169020]


class anti(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def ban(self, guild, user, *, reason: str = None):
        try:
            return await self.ban(guild, user, reason=reason)
        except Exception:
            return                  

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user) -> None:
        await self.client.wait_until_ready()

        if not guild:
            return
        if not guild.me.guild_permissions.view_audit_log:
            return
        async for entry in guild.audit_logs(limit=1,
                                            after=datetime.datetime.now() -
                                            datetime.timedelta(minutes=2),
                                            action=discord.AuditLogAction.ban):
            if entry.user.id in IGNORE or entry.user.id == guild.owner.id or entry.user.top_role >= guild.me.top_role:
                return
            else:
                if guild.me.guild_permissions.ban_members:
                    await guild.ban(entry.user,
                                   reason="Terminal | Anti Ban")
                    await guild.unban(user=user, reason="Terminal | Auto Recovery")                    

    @commands.Cog.listener()
    async def on_member_unban(self, guild: discord.Guild,
                              user: discord.User) -> None:
        await self.client.wait_until_ready()

        if not guild:
            return
        if not guild.me.guild_permissions.view_audit_log:
            return
        async for entry in guild.audit_logs(
                limit=1,
                after=datetime.datetime.now() - datetime.timedelta(minutes=2),
                action=discord.AuditLogAction.unban):
            if entry.user.id in IGNORE or entry.user.id == guild.owner.id or entry.user.top_role >= guild.me.top_role:
                return
            else:
                if guild.me.guild_permissions.ban_members:
                    await guild.ban(entry.user,
                                 reason="Terminal | Anti Unban")

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member) -> None:
        await self.client.wait_until_ready()

        guild = member.guild
        if not guild:
            return
        if not guild.me.guild_permissions.view_audit_log:
            return
        async for entry in guild.audit_logs(
                limit=1,
                after=datetime.datetime.now() - datetime.timedelta(minutes=2),
                action=discord.AuditLogAction.kick):
            if entry.user.id in IGNORE or entry.user.id == guild.owner.id or entry.user.top_role >= guild.me.top_role:
                return
            else:
                if guild.me.guild_permissions.ban_members:
                    await guild.ban(entry.user,
                                   reason="Terminal  | Anti Kick")

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:
        await self.client.wait_until_ready()

        guild = member.guild
        if not guild:
            return
        if not guild.me.guild_permissions.view_audit_log:
            return
        async for entry in guild.audit_logs(
                limit=1,
                after=datetime.datetime.now() - datetime.timedelta(minutes=2),
                action=discord.AuditLogAction.bot_add):
            if entry.user.id in IGNORE or entry.user.id == guild.owner.id or entry.user.top_role >= guild.me.top_role:
                return
            if member.bot:
                await member.ban(reason="Terminal | Anti Bot")
                if guild.me.guild_permissions.ban_members:
                    await guild.ban(entry.user,
                                   reason="Terminal | Anti Bot")
              
    @commands.Cog.listener()
    async def on_guild_update(self, after: discord.Guild,
                              before: discord.Guild) -> None:
        await self.client.wait_until_ready()

        guild = after
        if not guild:
            return
        if not guild.me.guild_permissions.view_audit_log:
            return
        async for entry in guild.audit_logs(
                limit=1,
                after=datetime.datetime.now() - datetime.timedelta(minutes=2),
                action=discord.AuditLogAction.guild_update):
            if entry.user.id in IGNORE or entry.user.id == guild.owner.id or entry.user.top_role >= guild.me.top_role:
                return
            else:
          #      await after.edit(name=f"{before.name}",
                                 #reason="Terminal | Recovery")
                if guild.me.guild_permissions.manage_webhooks:
                    await guild.ban(entry.user,
                                  reason="Terminal | Anti Guild Update")
                await after.edit(name=f"{before.name}",
                                 reason="Terminal | Recovery")
    @commands.Cog.listener()
    async def on_webhooks_update(self, channel) -> None:
        await self.client.wait_until_ready()

        guild = channel.guild
        if not guild:
            return
        if not guild.me.guild_permissions.view_audit_log:
            return
        async for entry in guild.audit_logs(
                limit=1,
                after=datetime.datetime.now() - datetime.timedelta(minutes=2),
                action=discord.AuditLogAction.webhook_create):
            if entry.user.id in IGNORE or entry.user.id == guild.owner.id or entry.user.top_role >= guild.me.top_role:
                return
            else:
                await guild.ban(entry.user,
                               reason="Terminal | Anti Guild Update")
                webhooks = await guild.webhooks()
                for webhook in webhooks:
                    if webhook.id == entry.target.id:
                        if guild.me.guild_permissions.manage_webhooks:
                            await webhook.delete()
                            break

    @commands.Cog.listener()
    async def on_guild_role_create(self, role) -> None:
        await self.client.wait_until_ready()

        guild = role.guild
        if not guild:
            return
        if not guild.me.guild_permissions.view_audit_log:
            return
        async for entry in guild.audit_logs(
                limit=1,
                after=datetime.datetime.now() - datetime.timedelta(minutes=2),
                action=discord.AuditLogAction.role_create):
            if entry.user.id in IGNORE or entry.user.id == guild.owner.id or entry.user.top_role >= guild.me.top_role:
                return
            else:
    #            await role.delete()
                if guild.me.guild_permissions.ban_members:
                    await guild.ban(entry.user,
                                   reason="Terminal | Anti Role Create")
                await role.delete()

def setup(client):
	client.add_cog(anti(client)) 
