# importing section 
import discord 
from discord.ext import commands,tasks
from discord.utils import get
import json, os
from random import choice
from PIL import Image
import asyncio, sys
from dotenv import load_dotenv
from webserver import keep_alive
from io import BytesIO
#.env code
load_dotenv()
token = os.getenv("DISCORD_TOKEN")

#setup
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.members = True
def get_prefix(client, message):
	with open("prefixes.json", "r") as f:
		prefixes = json.load(f)

	return prefixes[str(message.guild.id)]

def get_general_channel(client, channel):
	with open("generals.json", "r") as f:
		general_channels = json.load(f)
	
	return general_channels[str(channel.guild.id)]

client = commands.Bot(command_prefix=get_prefix , case_insenstive=True, intents=intents)
client.remove_command("help")

statuses = ["Hello There My Default Prefix Is .", "Eating", "Sleeping", "Grinding On Arena", "Man Why JS is TERRIBLE", "Python Is Better For Bots"]

#' events Section


@client.event
async def on_ready():
	change_status.start()
	print("the bot is ready")

initial_extensions = ["cogs.moderation"]

if __name__ == "__main__":
	for extension in initial_extensions:
		try:
			client.load_extension(extension)
		except Exception as e:
			print(f"failed to load the extension {extension}", file=sys.stderr)
			traceback.print_exc()


@tasks.loop(seconds=600)
async def change_status():
	await client.change_presence(activity=discord.Game(choice(statuses)), status=discord.Status.dnd)



@client.event
async def on_guild_join(ctx, guild):
	with open("prefixes.json", 'r') as f:
		prefixes = json.load(f)
	
	prefixes[str(guild.id)] = "."

	with open("prefixes.json", 'w') as f:
		json.dump(prefixes, f, indent=4)
	
	await ctx.send("Please Run `.setup` to see the instructions to config the bot")

@client.event
async def on_guild_remove(guild):
	with open("prefixes.json", "r") as f:
		prefixes = json.load(f)
	
	prefixes.pop(guild.id)



@client.event
async def on_member_join(ctx, member : discord.Member):
	welcome_image = Image.open("defaultImage.png")
	asset = member.avatar_url_as(size=120)
	data = BytesIO(await asset.read())
	pfp = Image.open(data)
	pfp = pfp.resize((292, 292))
	welcome_image.paste(pfp, (296, 160))
	welcome_image.save("welcome.png")
	welcome_send = await ctx.channel.send(f"Hello {member.mention} Welcome To Our Server\nStay Have a Good Time\nMember No.:{ctx.guild.member_count()} " , file=discord.File("welcome.png"))
	welcome_send.add_reaction("👋")

reactions_1 = [":heavy_check_mark:", ":heavy_multiplication_x:", "❎", "✅"]


@client.command()
async def setup(client, guild):
	embed = discord.Embed(title="Setup The Bot For This Server", description="Required Admin Permissions")
	embed.add_field(name=".prefix", value="To Set The Prefix Of The Bot `.prefix <new prefix>`", inline=False)
	embed.add_field(name=".general_channel", value="To Set The General Chat For The Auto-reply `.general_channel <the channel id only>`")


@client.command()
@commands.has_permissions(administrator=True)
async def general_channel(ctx, channel:discord.Guild.channels):
	with open("generals.json", "r") as f:
			generals = json.load(f)
	
	generals[str(ctx.guild.id)] = channel

	with open("generals.json", "w") as f:
		json.dump(generals, f, indent=4)
	
	await ctx.channel.send(f"The General Channel Has Been Specfied To THis Text Channel: <#{channel}>")









@client.command()
async def ping(ctx):
	await ctx.send(f"**Pong** The Ping Is {round(client.latency * 1000)}ms ")

@client.command()
@commands.has_permissions(manage_channels=True)
async def prefix(ctx, prefix):
	with open("prefixes.json", 'r') as f:
		prefixes = json.load(f)
	
	prefixes[str(ctx.guild.id)] = prefix

	with open("prefixes.json", 'w') as f:
		json.dump(prefixes, f, indent=4)
	
	await ctx.send(f"Prefix Changed To: `{prefix}`")

@client.command()
async def poll(ctx, *, question):
	embed = discord.Embed(title=f"{ctx.author} Has Added a Poll", color=0x87CEEB)
	embed.add_field(name="Poll:", value=f"          {question}")
	embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")

	oh_1 = await ctx.channel.send(embed=embed)
	await oh_1.add_reaction(reactions_1[3])
	await oh_1.add_reaction(reactions_1[2])
	await ctx.message.delete()

@client.command()
async def help(ctx, command_name=None):
	reactions = ["⬅️", "➡️"]

	embed = discord.Embed(title="         Help Command",description="Show The Help Command", color=0x87CEEB)
	embed.set_author(name="Gaming Bot", icon_url="https://m-albenaa.com/clientLounge/assets/loading/loading.gif")
	embed.add_field(name="Member Text Commands", value="Help\nId\nInfo\nPing\nPoll", inline=True)
	embed.add_field(name="Member Voice Commands", value="Join\nDisconnect", inline=True)
	embed.add_field(name="Admin Commands", value="Prefix\nMute\nBan\nUnban\nClear\nKick", inline=False)
	oh_cool = await ctx.send(embed=embed)
	await oh_cool.add_reaction(reactions[0])
	await oh_cool.add_reaction(reactions[1])






#voice channels commands

@client.command(pass_context=True)
async def join(ctx):
	if (ctx.author.voice):
		vchannel = ctx.message.author.voice.channel
		await vchannel.connect()
		await ctx.channel.send(":studio_microphone: Joined:white_check_mark: :studio_microphone:")
	else:
		ctx.author.send("You Are Not In a Voice Channel Boy")



@client.command(pass_context=True)
async def disconnect(ctx):
	if (ctx.voice_client):
		await ctx.guild.voice_client.disconnect()
		await ctx.send("I Left The Voice Channel:white_check_mark:")
	else:
		ctx.send("I'm Not A Voice Channel:joy:")


keep_alive()
client.run(token)
