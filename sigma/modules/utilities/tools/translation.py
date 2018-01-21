from sigma.core.mechanics.command import SigmaCommand
import discord
import translate


async def translation(cmd: SigmaCommand, message: discord.Message, args: list):
    if args:
        if len(args) >= 2:
            trans_arg = args[0]
            sentence = ' '.join(args[1:])
            if '>' in trans_arg:
                trans_split = trans_arg.split('>')
                from_lang = trans_split[0].lower()
                to_lang = trans_split[1].lower()
            else:
                from_lang = trans_arg
                to_lang = 'en'
            translator = translate.Translator(to_lang=to_lang, from_lang=from_lang)
            trans_output = translator.translate(sentence)
            title = f'🔠 Translated from {from_lang.upper()} to {to_lang.upper()}'
            response = discord.Embed(color=0x3B88C3, title=title)
            response.description = trans_output
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Missing language or sentence.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    await message.channel.send(embed=response)
