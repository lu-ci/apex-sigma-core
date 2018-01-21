from sigma.core.mechanics.command import SigmaCommand
import discord
from cryptography.fernet import Fernet, InvalidToken, InvalidSignature


async def encrypt(cmd: SigmaCommand, message: discord.Message, args: list):
    key = cmd.bot.cfg.pref.raw.get('key_to_my_heart')
    text = False
    if key:
        if args:
            if args[-1] == ':t':
                text = True
                crypt_text = ' '.join(args[:-1]).encode('utf-8')
            else:
                crypt_text = ' '.join(args).encode('utf-8')
            key = key.encode('utf-8')
            cipher = Fernet(key)
            try:
                ciphered = cipher.encrypt(crypt_text).decode('utf-8')
            except InvalidToken:
                ciphered = None
            except InvalidSignature:
                ciphered = None
            if ciphered:
                if text:
                    response = ciphered
                else:
                    response = discord.Embed(color=0xe75a70)
                    response.add_field(name=f'💟 Text Encrypted', value=ciphered)
            else:
                response = discord.Embed(color=0xBE1931, title='❗ The token or key are incorrect.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Nothing to decrypt.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ You don\'t posses a key.')
    if text:
        await message.channel.send(response)
    else:
        await message.channel.send(embed=response)
