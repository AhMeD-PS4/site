import discord 
from discord.ext import commands, tasks
import asyncio
import datetime


class ModCog(commands.Cog):

	def __init__(self, client):
		self.client = client

	@commands.command(description='- Mutes The Specified User (.mute <member> <time> <reason>)')
	async def mute(ctx, member : discord.Member, time, *, reason=None):
		guild = ctx.guild
		mutedRole = discord.utils.get(guild.roles, name="ππ¦π₯ππ πΉπͺ πΎπππππ πΉπ π₯")

		if not mutedRole:
			mutedRole = await guild.create_role(name="ππ¦π₯ππ πΉπͺ πΎπππππ πΉπ π₯")

			for channel in guild.channels:
				await channel.set_premission(mutedRole, speak=False, send_message=False, read_message=True)
		await member.add_roles(mutedRole, reason=reason)
		await ctx.channel.send(f"The Member '{member.mention}' Has Been Muted")

	@commands.command()
	@commands.has_permissions(kick_members=True)
	async def kick(ctx, member : discord.Member, *, reason=None):
		await member.kick(reason=reason)
		channel = ctx.channel
		await channel.send(f"{member.mention} βππ€ πΉπππ ππππππ!")

	@commands.command()
	@commands.has_permissions(ban_members=True)
	async def ban(self, ctx, member : discord.Member, *, reason=None):
		await member.ban(reason=reason)
		user = ctx.author
		channel = ctx.channel
		await channel.send(f"ππ€ππ£:{user.mention}βππ€ πΉπππ πΉπππππ βπ π£π£πππ₯ππͺ!\nReason:{reason}")


def setup(client):
	client.add_cog(ModCog(client))
	print("Moderation is loaded")






