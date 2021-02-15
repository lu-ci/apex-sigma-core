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

import codecs
import hashlib

from cryptography.fernet import Fernet


def get_encryptor(cfg):
    """
    :type cfg: sigma.core.mechanics.config.Configuration
    :rtype: cryptography.fernet.Fernet
    """
    cipher = None
    cipher_password = cfg.pref.raw.get('key_to_my_heart')
    if cipher_password:
        pass_hash = hashlib.new('md5')
        pass_hash.update(cipher_password.encode('utf-8'))
        pass_hash = pass_hash.hexdigest()
        pass_hash = codecs.encode(pass_hash.encode('utf-8'), 'base64')
        cipher = Fernet(pass_hash)
    return cipher
