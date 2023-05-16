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

import yaml


class Information(object):
    """
    An information wrapping class.
    """

    @staticmethod
    def get_version():
        """
        Grabs the version information class.
        :rtype: Version
        """
        return Version()

    @staticmethod
    def get_authors():
        """
        Grabs the author information class.
        :rtype: Authors
        """
        return Authors()

    @staticmethod
    def get_donors():
        """
        Grabs the donor information class.
        :rtype: Donors
        """
        return Donors()


class Version(object):
    """
    Version information containing wrapper class.
    """

    __slots__ = ("raw", "beta", "timestamp", "codename", "version", "major", "minor", "patch")

    def __init__(self):
        with open('info/version.yml', encoding='utf-8') as version_file:
            version_data = yaml.safe_load(version_file)
        self.raw = version_data
        self.beta = version_data.get('beta', False)
        self.timestamp = version_data.get('build_date', 0)
        self.codename = version_data.get('codename', 'Aurora')
        self.version = version_data.get('version', {})
        self.major = self.version.get('major', 0)
        self.minor = self.version.get('minor', 0)
        self.patch = self.version.get('patch', 0)


class Author(object):
    """
    Version information containing wrapper class.
    """

    __slots__ = ("name", "discriminator", "id")

    def __init__(self, author):
        """
        :type author: dict
        """
        self.name = author.get('name', 'Unknown')
        self.discriminator = author.get('discriminator', '0000')
        self.id = author.get('id', 0)


class Authors(object):
    """
    Author information containing wrapper class.
    """

    __slots__ = ("raw", "authors")

    def __init__(self):
        with open('info/authors.yml', encoding='utf-8') as authors_file:
            authors_data = yaml.safe_load(authors_file)
        self.raw = authors_data
        self.authors = []
        for author in authors_data:
            author_object = Author(author)
            self.authors.append(author_object)


class Donor(object):
    """
    Donor information containing wrapper class.
    """

    __slots__ = ("name", "tier", "avatar", "id")

    def __init__(self, donor):
        """
        Donor information containing wrapper class.
        :type donor: dict
        """
        self.name = donor.get('name', 'Unknown')
        self.tier = donor.get('tier', 0)
        self.avatar = donor.get('avatar')
        self.id = donor.get('duid', 0)


class Donors(object):
    """
    Contains and handles the loading of a list of donor files.
    """

    __slots__ = ("raw", "raw_list", "donors")

    def __init__(self):
        with open('info/donors.yml', encoding='utf-8') as donors_file:
            donors_data = yaml.safe_load(donors_file)
        self.raw = donors_data
        self.raw_list = donors_data.get('donors', [])
        self.donors = []
        for donor in self.raw_list:
            donor_object = Donor(donor)
            self.donors.append(donor_object)
