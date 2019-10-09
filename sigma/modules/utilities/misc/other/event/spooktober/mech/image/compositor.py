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

import abc
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont


class ImageCompositor(abc.ABC):
    __slots__ = ('canvas', 'font')

    def __init__(self, width, height):
        """
        Shorthand image compositing controller.
        :param width: The width of the canvas.
        :type width: int
        :param height: The height of the canvas.
        :type height: int
        """
        self.canvas = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        self.font = 'Exo2-Regular.ttf'

    def write(self, text, size, coordinates, color=(0, 0, 0)):
        """
        Writes some text on the image.
        :param text: The text to write.
        :type text: str
        :param size: The font size.
        :type size: int
        :param coordinates: The coordinates where to write the text.
        :type coordinates: tuple(int, int)
        :param color: The RGB color of the text, defaults to black.
        :type color: tuple(int, int, int)
        :return:
        :rtype:
        """
        font = ImageFont.truetype(self.font, size)
        draw = ImageDraw.Draw(self.canvas)
        draw.text(coordinates, text, font=font, fill=color)

    def text_image(self, text, size, color=(0, 0, 0)):
        """
        Makes a pastable PIL Image from text.
        :param text: The text to write.
        :type text: str
        :param size: The font size.
        :type size: int
        :param color: The RGB color of the text, defaults to black.
        :type color: tuple(int, int, int)
        :return:
        :rtype: PIL.Image.Image
        """
        base = Image.new('RGBA', (size * 2 * len(text), size * 2), (0, 0, 0, 0))
        font = ImageFont.truetype(self.font, size)
        draw = ImageDraw.Draw(base)
        tw, th = draw.textsize(text, font=font)
        true_base = Image.new('RGBA', (tw, th))
        true_draw = ImageDraw.Draw(true_base)
        true_draw.text((0, 0), text, font=font, fill=color)
        return true_base

    @staticmethod
    def resize(image, width=None, height=None):
        """
        Resizes an image proportionally if only one size is given.
        :param image: The image to resize.
        :type image: str or PIL.Image.Image
        :param height: The height to resize to.
        :type height: int
        :param width: The width to resize to.
        :type width: int
        :return:
        :rtype: PIL.Image.Image
        """
        if isinstance(image, str):
            image = Image.open(image)
        if height is None and width is None:
            return image
        iw, ih = image.size
        if height and width is None:
            width = int((height / ih) * iw)
        elif height is None and width:
            height = int((width / iw) * ih)
        return image.resize((width, height), Image.ANTIALIAS)

    def stick(self, what, where, mask=None):
        """
        Sticks an image by path to a location.
        :param what: The image to paste onto the canvas.
        :type what: str or PIL.Image.Image
        :param where: The location where to paste it.
        :type where: tuple(int, int)
        :param mask: The image mask if there is one.
        :type mask: str or PIL.Image.Image
        :return:
        :rtype:
        """
        if isinstance(what, str):
            pasty = Image.open(what)
        else:
            pasty = what
        if mask:
            if isinstance(mask, str):
                masky = Image.open(mask)
            else:
                masky = mask
            self.canvas.paste(pasty, where, masky)
        else:
            self.canvas.paste(pasty, where, pasty)

    def to_bytes(self):
        io = BytesIO()
        self.canvas.save(io, format="PNG")
        io.seek(0)
        return io

    def save(self, out=None):
        self.canvas.save(out if out else 'test.png', format='PNG')
