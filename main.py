import discord
from discord.ext import commands, tasks

client - commands.Bot(command_prefix=".")


@client.event 
async def on_ready():
    print("the bot is online")


@client.event
async def on_member_join(member : discord.Member):
    


