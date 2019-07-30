"""
Apex Sigma: The Database Giant Discord Bot.
Copyright (C) 2019  Lucia's Cipher

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import datetime
import os

import aiml
import arrow
import yaml

chatter_core = aiml.Kernel()
chatter_core.verbose(False)


def cb_log(ev, init, text):
    """
    Logs a chatterbot core initialization line.
    :param ev: The event object references in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    :param init: If the training is initializing or runtime.
    :type init: boot
    :param text: The text to log.
    :type text: str
    :return:
    :rtype:
    """
    if init:
        ev.log.info(text)


def train(ev, core, init=False):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    :param core: The chatterbot core class.
    :type core: aiml.Kernel
    :param init: If the training is initializing or runtime.
    :type init: bool
    """
    cb_log(ev, init, 'Learning generic AIML interactions...')
    core.learn(os.sep.join([ev.resource(f'aiml_files'), '*.aiml']))
    cb_log(ev, init, 'Learning properties unique to the client...')
    with open(ev.resource('properties.yml')) as prop_file:
        prop_data = yaml.safe_load(prop_file)
    for prop_key in prop_data:
        prop_val = prop_data.get(prop_key)
        chatter_core.setBotPredicate(prop_key, prop_val)
    cb_log(ev, init, 'Learning additional software details...')
    version = ev.bot.info.get_version()
    full_version = f'{version.major}.{version.minor}.{version.patch}'
    if version.beta:
        full_version += ' Beta'
    chatter_core.setBotPredicate('version', full_version)
    birthday_date = arrow.get(datetime.date(2016, 8, 16))
    age = (arrow.utcnow() - birthday_date).days // 365.25
    chatter_core.setBotPredicate('age', str(int(age)))
    chatter_core.setBotPredicate('birthday', birthday_date.format('MMMM DD'))
    chatter_core.setBotPredicate('birthdate', birthday_date.format('MMMM DD, YYYY'))
    cb_log(ev, init, 'Loaded Chatter Core.')


async def chatter_core_init(ev):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    """
    ev.log.info('Training chatter core...')
    train(ev, chatter_core, True)
    ev.log.info('Chatter core training finished.')
