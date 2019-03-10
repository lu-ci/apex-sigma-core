# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2019  Lucia's Cipher
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

import os

import aiml
import arrow
import yaml

from sigma.core.mechanics.event import SigmaEvent

chatter_core = aiml.Kernel()
chatter_core.verbose(False)


def train(ev: SigmaEvent, core):
    aiml_files = sorted(os.listdir(ev.resource('aiml_files')))
    for aiml_file in aiml_files:
        core.learn(ev.resource(f'aiml_files/{aiml_file}'))


async def chatter_core_init(ev: SigmaEvent):
    train(ev, chatter_core)
    with open(ev.resource('properties.yml')) as prop_file:
        prop_data = yaml.safe_load(prop_file)
    for prop_key in prop_data:
        prop_val = prop_data.get(prop_key)
        chatter_core.setBotPredicate(prop_key, prop_val)
    ver_nest = ev.bot.info.get_version().raw.get('version')
    full_version = f'{ver_nest.get("major")}.{ver_nest.get("minor")}.{ver_nest.get("patch")}'
    chatter_core.setBotPredicate('version', full_version)
    birthday_date = arrow.get('2016-08-16', format='YYYY-MM-DD')
    age = (arrow.utcnow() - birthday_date).days // 365.25
    chatter_core.setBotPredicate('age', age)
    chatter_core.setBotPredicate('birthday', birthday_date.format('MMMM DD'))
    chatter_core.setBotPredicate('birthdate', birthday_date.format('MMMM DD, YYYY'))
    chatter_core.setBotPredicate('name', ev.bot.user.name)

