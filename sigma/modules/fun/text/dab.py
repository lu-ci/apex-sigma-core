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


async def dab(cmd, message, args):
    faces = [
        ' ( ˙-˙ )', '( ﾟ_ﾟ )', '（・・）', '( ・-・ )', '（・＿・)',
        '(ʘᗩʘ’)', '◎ܫ◎', '（゜◇゜）', '꒪ꄱ꒪', 'Σ(O_O；)', 'ಠ_ಠ',
        'ಠ_ಠ', '⋋_⋌', '눈_눈', 'ಠ⌣ಠ', 'ಠ▃ಠ', 'ఠ', '͟ಠ', 'ಠ_ರೃ',
        'ノಠ_ಠノ', '(¬_¬)', '(｀ε´)', '(ಠ⌣ಠ)', '(◣_◢)', '(¬▂¬)',
        '(┳◇┳)', '(눈_눈)', '(¬､¬)', '(\`A´)', '（▽д▽）', '-\`д´-',
        '(’益’)', '(⋋▂⋌)', '〴⋋_⋌〵', '(◔', 'д◔)', '(◞‸◟；)',
        '☜(\`o´)', '(ಥ_ʖಥ)', '(ʘдʘ╬)', '（♯▼皿▼）', '(｀Д´)',
        '(#｀皿´)', '(¬_¬)ﾉ', '(╬ಠ益ಠ)', '(ಠ', '∩ಠ)', '(', '>д<)',
        '凸(¬‿¬)', '(⁎˃ᆺ˂)', '凸ಠ益ಠ)凸', '(；¬д¬)', '(-_-｡)',
        '(º言º)', 'ლಠ益ಠ)ლ', '(≧Д≦)', '(°ㅂ°╬)', '（｀Δ´）！',
        '(ᗒᗣᗕ)՞', '（#＾ω＾）', '（▼へ▼メ）', '(╬⓪益⓪)', '(#\`皿´)'
    ]
    face = secrets.choice(faces)
    signs = ['.', '...', '!', '!!!']
    sign = secrets.choice(signs)
    output = f'`{face}` No{sign}'
    await message.channel.send(output)
