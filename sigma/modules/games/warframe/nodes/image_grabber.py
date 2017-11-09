import aiohttp
from lxml import html


async def grab_image(name, cut=False):
    base_url = 'http://warframe.wikia.com/wiki'
    if ' Blueprint' in name:
        name = name.replace(' Blueprint', '')
    name = name.replace(' ', '_')
    if cut:
        name = '_'.join(name.split('_')[:-1])
    check_name = name.split('_')
    try:
        int(check_name[0])
        resource = True
    except IndexError:
        resource = False
    if resource:
        name = '_'.join(check_name[1:])
    item_url = f'{base_url}/{name}'
    async with aiohttp.ClientSession() as session:
        async with session.get(item_url) as data:
            page_data = await data.read()
    root = html.fromstring(page_data)
    img_objects = root.cssselect('.image')
    img_object = None
    for obj in img_objects:
        if 'href' in obj.attrib:
            if obj.attrib['href'].startswith('http'):
                if 'prime-access' not in obj.attrib.get('href'):
                    img_object = obj
                    break
    if img_object is not None:
        img_url = img_object.attrib['href']
    else:
        img_url = 'https://i.imgur.com/99ennZD.png'
    return img_url


async def alt_grab_image(name, cut=False):
    base_url = 'http://warframe.wikia.com/wiki'
    if ' Blueprint' in name:
        name = name.replace(' Blueprint', '')
    name = name.replace(' ', '_')
    if cut:
        name = '_'.join(name.split('_')[:-1])
    item_url = f'{base_url}/{name}'
    async with aiohttp.ClientSession() as session:
        async with session.get(item_url) as data:
            page = await data.text()
    root = html.fromstring(page)
    try:
        item_image = root.cssselect('.infobox')[0][1][0][0].attrib.get('href')
    except IndexError:
        item_image = root.cssselect('.pi-image-thumbnail')[0].attrib.get('src')
    return item_image
