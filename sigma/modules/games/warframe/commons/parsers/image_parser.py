import aiohttp
from lxml import html


class FailedIconGrab(Exception):
    def __init__(self):
        self.message = 'Failed to grab an image due to a key or index error.'


def remove_revision(url):
    dot_split = url.split('.')
    pre_ext = '.'.join(dot_split[:-1])
    post_ext = dot_split[-1]
    ext = post_ext.split('/')[0]
    out_url = f'{pre_ext}.{ext}'
    return out_url


async def grab_image(name):
    try:
        page_url = f'http://warframe.wikia.com/wiki/{name}'
        async with aiohttp.ClientSession() as session:
            async with session.get(page_url) as item_page_call:
                item_html = await item_page_call.text()
        item_page = html.fromstring(item_html)
        img_element = item_page.cssselect('.pi-image-thumbnail')[0]
        img_url = remove_revision(img_element.attrib.get('src'))
    except (IndexError, KeyError):
        raise FailedIconGrab
    return img_url
