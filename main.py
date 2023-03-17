import discord
from discord.ext import commands, tasks
from discord.voice_client import VoiceClient
import random
import time
import os
import asyncio
from data import *
import youtube_dl
import logging
from pathlib import Path
import platform
import json
import datetime


cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n-----")

def get_prefix(client, message):
    return ["-", "+"]

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix=get_prefix, case_insensitive=True, owner_id = 862374422749249556,intents=intents)

client.colors = [
  0xFFFFFF,
  0x1ABC9C,
  0x2ECC71,
  0x3498DB,
  0x9B59B6,
  0xE91E63,
  0xF1C40F,
  0xE67E22,
  0xE74C3C,
  0x34495E,
  0x11806A,
  0x1F8B4C,
  0x206694,
  0x71368A,
  0xAD1457,
  0xC27C0E,
  0xA84300,
  0x992D22,
  0x2C3E50
  ]


client.version = "0.3.1"


@client.event
async def on_ready():
    await client.change_presence(
        status=discord.Status.idle,
        activity=discord.Game("dead | -help"))
    print(f"We have logged in as {client.user}")


@client.event
async def on_command_error(ctx,error):
  ignored = (commands.CommandNotFound, commands.UserInputError)
  if isinstance(error, ignored):
    return

  elif isinstance(error, commands.CommandOnCooldown):
    m, s= divmod(error.retry_after , 60)
    h, m= divmod(m, 60)
    if int(h) == 0 and int(m)==0:
      await ctx.send(f"You must wait {int(s)} seconds to use this command")
    elif int(h) == 0 and int(m) != 0:
      await ctx.send(f"You have to wait {int(m)} minutes and {int(s)} seconds to use this command")
    else:
      await ctx.send(f"You wait {int(h)} hours, {int(m)} minutes and {int(s)} seconds to use this commands")
  elif isinstance(error, commands.CheckFailure):
    await ctx.send("You lack the permission to use this command")
  raise error


for filename in os.listdir("./cogs"):
  if filename.endswith(".py") and not filename.startswith("_"):
    client.load_extension(f"cogs.{filename[:-3]}")

client.run(TOKEN)
