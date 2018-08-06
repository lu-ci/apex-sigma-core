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

import json
import arrow
import string
from queue import Queue

import pymongo

start_time = arrow.utcnow()
last_time = arrow.utcnow()


def slugify(text: str):
    charlist = enumerate(list(text))
    last_capital = False
    new_charlist = []
    for index, char in charlist:
        if not last_capital:
            if index == 0:
                new_charlist.append(char.lower())
            else:
                if char.upper() == char and char in string.ascii_letters:
                    new_charlist += ['_', char.lower()]
                else:
                    new_charlist.append(char.lower())
        else:
            new_charlist.append(char.lower())
        last_capital = char.upper() == char
    return ''.join(new_charlist)


with open('keys.json') as kfile:
    keydata = json.loads(kfile.read())
    keydoc = {}
    for item in keydata:
        keydoc.update(item)


def slugify_doc(doc: dict):
    new_doc = {}
    slugged = 0
    skipped = 0
    for key in doc:
        newkey = keydoc.get(key) if keydoc.get(key) else key
        val = doc.get(key)
        if key != newkey:
            slugged += 1
        else:
            skipped += 1
        if isinstance(val, dict):
            val, sl, sk = slugify_doc(val)
            slugged += sl
            skipped += sk
        elif isinstance(val, list):
            val_list = []
            for subdoc in val:
                sval = subdoc
                if isinstance(subdoc, dict):
                    sval, sl, sk = slugify_doc(subdoc)
                    slugged += sl
                    skipped += sk
                val_list.append(sval)
            val = val_list
        new_doc.update({newkey: val})
    return new_doc, slugged, skipped


all_keys = []
xk = []


def is_number(key):
    num = False
    for itype in [8, 10, 16]:
        try:
            int(key, itype)
            num = True
            break
        except ValueError:
            pass
    return num


def add_key_to_list(key):
    if key.lower() != key and not is_number(key):
        if key not in all_keys:
            all_keys.append(key)


def get_key_list(doc):
    q = Queue()
    q.put(doc)
    while not q.empty():
        d = q.get()
        for key in d:
            add_key_to_list(key)
            val = doc.get(key)
            if isinstance(val, dict):
                q.put(val)
            elif isinstance(val, list):
                for sval in val:
                    if isinstance(sval, dict):
                        q.put(sval)


def caps_in_doc(doc):
    caps = False
    for key in doc:
        val = doc.get(key)
        if isinstance(val, dict):
            caps = caps_in_doc(val)
        elif isinstance(val, list):
            for sval in val:
                if isinstance(sval, dict):
                    caps = caps_in_doc(sval)
        if key.lower() != key:
            caps = True
        if caps:
            break
    return caps


def has_any_caps(docs):
    caps = False
    for doc in docs:
        caps = caps_in_doc(doc)
        if caps:
            break
    return caps


def print_progress(tsl, tsk, ter):
    global last_time
    now = arrow.utcnow()
    if last_time.timestamp + 1 < now.float_timestamp:
        last_time = now
        diff = now.timestamp - start_time.timestamp
        print(f'Ongoing... Slugged: {tsl} | Skipped: {tsk} | Errored: {ter} | Elapsed: {diff}s...')


def run(db_addr, skippable):
    db = pymongo.MongoClient(db_addr)
    colls = list(sorted(db.aurora.list_collections(), key=lambda x: x.get('name')))
    curr = 0
    total = len(colls)
    print(f'Slugging {total} collections.')
    for coll in colls:
        coll_nam = coll.get('name')
        tsl, tsk, ter = 0, 0, 0
        if coll_nam not in skippable:
            collx = db.aurora[coll_nam]
            print(f'Slugging {coll_nam}...')
            docs = list(collx.find())
            print('Checking cap presence...')
            if has_any_caps(docs):
                print('Iterating documents for cleaning...')
                for doc in docs:
                    print_progress(tsl, tsk, ter)
                    sdoc, slugged, skipped = slugify_doc(doc)
                    tsl += slugged
                    tsk += skipped
                    try:
                        collx.delete_one(doc)
                        collx.insert_one(sdoc)
                    except Exception:
                        collx.insert_one(doc)
                        ter += 1
            else:
                print(f'Skipping {coll_nam} cause no non-snake_case keys present.')
        else:
            print(f'Skipping {coll_nam} cause skippable.')
        curr += 1
        print(f'{coll.get("name")} - Slugged: {tsl} | Skipped: {tsk} | Errored: {ter} | {curr}/{total}')
    print(f'Slugged {len(all_keys)} non-snake_case database keys.')


# Your mongo address goes here and list of things you want to skip
run('mongodb://localhost:27017', ['Errors', 'MarkovChains'])

