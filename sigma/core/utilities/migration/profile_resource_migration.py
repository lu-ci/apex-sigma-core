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

import pymongo


def set_resources(db, uid, name, data):
    resources = db.aurora[f'{name.title()}Resource'].find_one({'user_id': uid})
    coll = db.aurora[f'{name.title()}Resource']
    if resources:
        coll.update_one({'user_id': uid}, {'$set': data})
    else:
        data.update({'user_id': uid})
        coll.insert_one(data)


def set_inventory(db, uid, inv):
    inventory = db.sigma.Inventory.find_one({'user_id': uid})
    if inventory:
        db.sigma.Inventory.update_one({'user_id': uid}, {'$set': {'items': inv}})
    else:
        db.sigma.Inventory.insert_one({'user_id': uid, 'items': inv})


def get_clean_profiles(profs):
    clean_profs = []
    for prof in profs:
        if 'chevrons' in prof or 'spouses' in prof or 'upgrades' in prof:
            if 'inventory' in prof:
                prof.pop('inventory')
            if 'resources' in prof:
                prof.pop('resources')
            clean_profs.append(prof)
    print(f'Found {len(clean_profs)} good profiles.')
    return clean_profs


def run(db_addr):
    db = pymongo.MongoClient(db_addr)
    profiles = list(db.sigma.Profiles.find())
    pcount = len(profiles)
    print(f'Grabbed {pcount} profiles.')
    pind = 0
    for profile in profiles:
        pind += 1
        uid = profile.get('user_id')
        reses = profile.get('resources', {})
        for rkey in reses:
            resdat = reses.get(rkey)
            set_resources(db, uid, rkey, resdat)
            print(f'Transfered {uid}\'s {rkey} data... | {pind}/{pcount}')
        inv = profile.get('inventory', [])
        if inv:
            set_inventory(db, uid, inv)
            print(f'Transfered {uid}\'s inventory data... | {pind}/{pcount}')

    cleans = get_clean_profiles(profiles)
    db.sigma.Profiles.drop()
    db.sigma.Profiles.insert_many(cleans)


# Your mongo address goes here
run('mongodb://localhost:27017')
