import discord
from geopy.geocoders import Nominatim

map_icon = 'https://i.imgur.com/zFl9UPx.jpg'


async def mapsearch(cmd, message, args):
    if args:
        search = ' '.join(args)
        search_url = '+'.join(args)
        if search:
            geo_parser = Nominatim()
            location = geo_parser.geocode(search)
            if location:
                lat = location.latitude
                lon = location.longitude
                maps_url = f'https://www.google.rs/maps/search/{search_url}/@{lat},{lon},11z?hl=en'
                response = discord.Embed(color=0xdd4e40)
                response.set_author(name=f'{location}', icon_url=map_icon, url=maps_url)
            else:
                maps_url = f'https://www.google.rs/maps/search/{search_url}'
                response = discord.Embed(color=0xdd4e40)
                response.set_author(name=f'Broad Search: {search.title()}', icon_url=map_icon, url=maps_url)
        else:
            response = discord.Embed(color=0xBE1931, title='❗ No location inputted.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    await message.channel.send(embed=response)
