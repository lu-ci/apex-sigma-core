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
import secrets

import discord

from sigma.modules.searches.safebooru.mech.safe_core import grab_post_list, generate_embed

links = []
embed_titles = ['Nyaa~', 'Nyanpasu!', 'Mnya :3', 'Meow~', '(｡･ω･｡)', 'ὃ⍜ὅ', 'ㅇㅅㅇ',
                'චᆽච', 'ऴिाी', '(ФДФ)', '（ΦωΦ）', '(ꀄꀾꀄ)', 'ฅ•ω•ฅ', '⋆ටᆼට⋆', '(ꅈꇅꅈ)',
                '<ΦωΦ>', '（ФоФ)', '(^人^)', '(ꀂǒꀂ)', '(・∀・)', '(ꃪꄳꃪ)', '=ටᆼට=',
                '(ΦεΦ)', 'ʘ̥ꀾʘ̥', '(ΦёΦ)', '=ộ⍛ộ=', '(Ф∀Ф)', '(ↀДↀ)', '(Φ_Φ)', '^ↀᴥↀ^',
                'โ๏∀๏ใ', '(Φ∇Φ)', '[ΦωΦ]', '(ΦωΦ)', 'ミ๏ｖ๏彡', '(ΦзΦ)', '|ΦωΦ|',
                '(⌯⊙⍛⊙)', 'ि०॰०ॢी', '=^∇^*=', '(⁎˃ᆺ˂)', '(ㅇㅅㅇ❀)', '(ノω<。)',
                '(ↀДↀ)✧', 'ि०॰͡०ी', 'ฅ(≚ᄌ≚)', '(=･ｪ･=?', '(^･ｪ･^)', '(≚ᄌ≚)ƶƵ',
                '(○｀ω´○)', '(●ↀωↀ●)', '(｡･ω･｡)', '(*Φ皿Φ*)', '§ꊘ⃑٥ꊘ⃐§', ']*ΦωΦ)ノ']


async def nekomimi(cmd, message, args):
    global links
    if not links:
        filler_message = discord.Embed(color=0xff6699, title='🐱 One moment, filling Sigma with catgirls...')
        fill_notify = await message.channel.send(embed=filler_message)
        links = await grab_post_list('cat_ears')
        filler_done = discord.Embed(color=0xff6699, title=f'🐱 We added {len(links)} catgirls!')
        await fill_notify.edit(embed=filler_done)
    rand_pop = secrets.randbelow(len(links))
    post_choice = links.pop(rand_pop)
    icon = 'https://3.bp.blogspot.com/_SUox58HNUCI/SxtiKLuB7VI/AAAAAAAAA08/s_st-jZnavI/s400/Azunyan+fish.jpg'
    response = generate_embed(post_choice, embed_titles, icon=icon)
    await message.channel.send(None, embed=response)
