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
from sigma.core.mechanics.fetch import get_fetch_helper


def has_changed(before, after):
    """
    Checks basic details before trying
     to generate a document or touch the database
    :param before: The user's previous state.
    :type before: discord.Member
    :param after: The user's current state.
    :type after: discord.Member
    :return:
    :rtype: bool
    """
    if before.name == after.name:
        if before.discriminator == after.discriminator:
            if before.avatar == after.avatar:
                return False
    return True


async def user_updater(ev, pld):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    :param pld: The event payload data to process.
    :type pld: sigma.core.mechanics.payload.MemberUpdatePayload
    """
    variant = 'user'
    if has_changed(pld.before, pld.after):
        fh = get_fetch_helper(ev.bot)
        data = fh.make_user_data(pld.after)
        await fh.save_object_doc(variant, data)
