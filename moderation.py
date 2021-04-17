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
		mutedRole = discord.utils.get(guild.roles, name="𝕄𝕦𝕥𝕖𝕕 𝔹𝕪 𝔾𝕒𝕞𝕚𝕟𝕘 𝔹𝕠𝕥")

		if not mutedRole:
			mutedRole = await guild.create_role(name="𝕄𝕦𝕥𝕖𝕕 𝔹𝕪 𝔾𝕒𝕞𝕚𝕟𝕘 𝔹𝕠𝕥")

			for channel in guild.channels:
				await channel.set_premission(mutedRole, speak=False, send_message=False, read_message=True)
		await member.add_roles(mutedRole, reason=reason)
		await ctx.channel.send(f"The Member '{member.mention}' Has Been Muted")

	@commands.command()
	@commands.has_permissions(kick_members=True)
	async def kick(ctx, member : discord.Member, *, reason=None):
		await member.kick(reason=reason)
		channel = ctx.channel
		await channel.send(f"{member.mention} ℍ𝕒𝕤 𝔹𝕖𝕖𝕟 𝕂𝕚𝕔𝕜𝕖𝕕!")

	@commands.command()
	@commands.has_permissions(ban_members=True)
	async def ban(self, ctx, member : discord.Member, *, reason=None):
		await member.ban(reason=reason)
		user = ctx.author
		channel = ctx.channel
		await channel.send(f"𝕌𝕤𝕖𝕣:{user.mention}ℍ𝕒𝕤 𝔹𝕖𝕖𝕟 𝔹𝕒𝕟𝕟𝕖𝕕 ℂ𝕠𝕣𝕣𝕖𝕔𝕥𝕝𝕪!\nReason:{reason}")


def setup(client):
	client.add_cog(ModCog(client))
	print("Moderation is loaded")






