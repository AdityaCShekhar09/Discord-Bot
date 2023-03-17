import discord
from discord.ext import commands
import random
import cogs._json


class Permission_Required(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Permission_Required Cog has loaded")

    @commands.command(name="kick", help="Kicks someone")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *,reason=None):
        data = cogs._json.read_json("blacklist.json")
        if ctx.author.id in data["blacklistedUsers"]:
          return
        if reason==None:
            reason=" no reason provided"
        await ctx.send(f'User {member.mention} has been kicked for {reason}')  
        await ctx.guild.kick(member)

    @commands.command(name="ban", help="Bans someone")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        data = cogs._json.read_json("blacklist.json")
        if ctx.author.id in data["blacklistedUsers"]:
          return
        if reason == None:
          reason = "no reason provided"
        await ctx.send(f"Banned {member.mention} has been ban for {reason}")
        await member.ban(reason=reason)

    @commands.command(name="unban", help="unbans someone")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        data = cogs._json.read_json("blacklist.json")
        if ctx.author.id in data["blacklistedUsers"]:
          return
        banned_users = await ctx.guild.bans()
        member_name, discriminator = member.split("#")
        for entry in banned_users:
            user = entry.user
            if (user.name, user.discriminator) == (member_name, discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f"Unbaned {user.mention}")
                return


def setup(client):
    client.add_cog(Permission_Required(client))
