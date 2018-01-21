import discord

from sigma.core.mechanics.command import SigmaCommand


async def donate(cmd: SigmaCommand, message: discord.Message, args: list):
    sigma_title = 'Sigma Donation Information'
    donation_url = f'{cmd.bot.cfg.pref.website}/donate'
    response = discord.Embed(color=0x1B6F5F, title=sigma_title)
    response.description = f'Care to help out? Come [support]({donation_url}) Sigma!'
    await message.channel.send(embed=response)
