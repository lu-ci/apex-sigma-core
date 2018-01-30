# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2017  Lucia's Cipher
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

def log_dm(ev, message):
    author_text = f'{message.author.name}#{message.author.discriminator} [{message.author.id}]'
    ev.log.info(f'DM From {author_text}: {message.content}')


async def dm_detection(ev, message):
    if not message.guild:
        if not message.author.bot:
            pfx = await ev.bot.get_prefix(message)
            if not message.content.startswith(pfx):
                log_dm(ev, message)
                if not await ev.bot.cool_down.on_cooldown(ev.name, message.author):
                    await ev.bot.modules.commands['help'].execute(message, [])
                    await ev.bot.cool_down.set_cooldown(ev.name, message.author, 30)
