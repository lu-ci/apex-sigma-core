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


class VisualNovel(object):
    def __init__(self, page_root):
        """
        :type page_root: lxml.html.HtmlElement
        """
        self.page = page_root
        self.id = self.page.base.split('/')[-1][1:]
        self.url = f'https://vndb.org/v{self.id}'
        self.details = self.page.cssselect('.vndetails')[0]
        self.detail_table = self.details[1]
        self.title = self.title_from_details(self.detail_table)
        self.aliases = self.detail_table[1][1].text.split(', ')
        self.length = self.detail_table[2][1].text
        self.image = None
        self.nsfw = False
        self.get_image()
        self.tags = []
        self.get_tags()
        self.description = self.page.cssselect('.vndesc')[0][1].text_content().split('[')[0]
        if len(self.description) >= 1024:
            self.description = f'{self.description[:1021]}...'
        self.screenshots = []
        self.nsfw_screenshots = []
        self.get_screenshots()

    @staticmethod
    def title_from_details(details):
        out = None
        titles = details.cssselect('.title')
        # Try english first.
        for title in titles:
            lang = title[1][0].attrib.get('lang')
            if lang is None:
                out = title[1][0].text.strip()
                break
        if out is None:
            for title in titles:
                lang = title[1][0].attrib.get('lang')
                if lang.startswith('ja'):
                    out = title[1][0].text.strip()
                    break
        return out

    def get_tags(self):
        self.tags = []
        proto_tags = [tag for tag in self.page.cssselect('#vntags')[0].text_content().split('.')]

        for proto_tag in proto_tags:
            tag_pieces = proto_tag.split()
            try:
                int(tag_pieces[0])
                proto_tag = proto_tag[1:]
            except ValueError:
                pass
            try:
                int(tag_pieces[-1])
                proto_tag = proto_tag[:-1]
            except ValueError:
                pass
            self.tags.append(proto_tag)
        self.tags = [stag.strip() for stag in self.tags]

    def get_image(self):
        try:
            vn_image_proto = self.details[0]
            try:
                nsfw_image_proto = self.page.cssselect('#nsfw_hid')[0]
            except IndexError:
                nsfw_image_proto = []
            if len(nsfw_image_proto):
                self.image = nsfw_image_proto[0].attrib.get('src')
                self.nsfw = True
            else:
                self.image = vn_image_proto[0].attrib.get('src')
                self.nsfw = False
        except IndexError:
            pass

    def get_screenshots(self):
        try:
            screen_links = self.page.cssselect('.scrlnk')
            for slink in screen_links:
                if slink.attrib.get('class') == 'scrlnk nsfw':
                    self.nsfw_screenshots.append(slink.attrib.get('href'))
                else:
                    self.screenshots.append(slink.attrib.get('href'))
        except IndexError:
            pass
