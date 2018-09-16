# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2018  Lucia's Cipher
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
import pymongo


def get_profile(db, uid):
    return db.sigma.Profiles.find_one({'user_id': uid}) or {}


def set_profile(db, uid, data):
    exists = db.sigma.Profiles.find_one({'user_id': uid})
    if exists:
        db.sigma.Profiles.update_one({'user_id': uid}, {'$set': data})
    else:
        data.update({'user_id': uid})
        db.sigma.Profiles.insert_one(data)


def set_resources(db, uid, name, data):
    profile = get_profile(db, uid)
    resources = profile.get('resources') or {}
    resources.update({name: data})
    set_profile(db, uid, {'resources': resources})


def transfer_cookies(db):
    cdocs = list(db.sigma.Cookies.find())
    li = 0
    ti = len(cdocs)
    for cdoc in cdocs:
        li += 1
        uid = cdoc.get('user_id')
        cks = cdoc.get('cookies')
        ttl = cdoc.get('total')
        data = {'current': cks, 'total': ttl}
        set_resources(db, uid, 'cookies', data)
        print(f'[{li}/{ti}] Transfered {uid}\'s cookies...')


def transfer_currency(db):
    cdocs = list(db.sigma.CurrencySystem.find())
    li = 0
    ti = len(cdocs)
    for cdoc in cdocs:
        li += 1
        uid = cdoc.get('user_id')
        crk = cdoc.get('current')
        ttl = cdoc.get('total')
        rnk = cdoc.get('global')
        gld = cdoc.get('guilds')
        data = {'current': crk, 'total': ttl, 'ranked': rnk, 'origins': {'guilds': gld}}
        set_resources(db, uid, 'currency', data)
        print(f'[{li}/{ti}] Transfered {uid}\'s currency...')


def transfer_inventory(db):
    cdocs = list(db.sigma.Inventory.find())
    li = 0
    ti = len(cdocs)
    for cdoc in cdocs:
        li += 1
        uid = cdoc.get('user_id')
        inv = cdoc.get('items')
        data = {'inventory': inv}
        set_profile(db, uid, data)
        print(f'[{li}/{ti}] Transfered {uid}\'s inventory...')


def transfer_upgrades(db):
    cdocs = list(db.sigma.Upgrades.find())
    li = 0
    ti = len(cdocs)
    for cdoc in cdocs:
        li += 1
        uid = cdoc.get('user_id')
        cdoc.pop('_id')
        cdoc.pop('user_id')
        set_profile(db, uid, {'upgrades': cdoc})
        print(f'[{li}/{ti}] Transfered {uid}\'s upgrades...')


def run(db_addr):
    db = pymongo.MongoClient(db_addr)
    transfer_cookies(db)
    transfer_currency(db)
    transfer_inventory(db)
    transfer_upgrades(db)


# Your mongo address goes here
run('mongodb://localhost:27017')
