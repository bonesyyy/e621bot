import discord
import aiohttp
import json
import random
from typing import Optional
from requests.auth import HTTPBasicAuth
from aiohttp import request
from aiohttp import BasicAuth
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import MinimalHelpCommand

MY_GUILD = discord.Object(id=993341337158025238)

client = commands.Bot(command_prefix = '/', intents = discord.Intents.all(), application_id = '958595938425929818', activity = discord.Game(name="with your mom | /help"))

class client(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)

client = client()

@client.event
async def on_ready():
    print(f'logged in as {client.user}')

# @client.tree.command(brief='You can add tags with >e621 <tag>+<tag>',
#                 description='You can use tags by doing >e621 <tag>+<tag>\n\n'
#                 'An example would be >e621 male/male+hair+blush')

@client.tree.command(name="e621", description="Fetches images from e621")
async def e621(interaction: discord.Interaction, tags: Optional[str]):

    headers = {
        'User-Agent': 'bonesproject/1.0 by bonesyyy',
    }

    try:
        args = (" ".join(map(str,tags)))
    except:
        print("No tags present")

    if tags == None:
        image_url = f"https://e621.net/posts.json?limit=100/"
    else:
        image_url = f"https://e621.net/posts.json?limit=100&tags={tags}"

    async with request("GET", image_url,auth=BasicAuth('bonesyyy', 'AUTH_TOKEN'), headers=headers) as response:
        #await ctx.send(f"API returned a {response.status} status")
        try:
            if response.status == 200:
                data = await response.json()
                count = len(data['posts'])
                r = random.randint(0,count)
                id = data['posts'][r]['id']
                score = data['posts'][r]['score']['total']
                width = data['posts'][r]['file']['width']
                height = data['posts'][r]['file']['height']
                ext = data['posts'][r]['file']['ext']
                image_link = data['posts'][r]['file']['url']
        except:
            image_link = None
            await interaction.response.send_message(f'There was no post containing the tags: {tags}')
            # await ctx.send(f"There was no post containing the tags: {tags}")

        embed = discord.Embed(title=f"{tags}", description=f'[Link](https://e621.net/posts/{id}/) | Score: {score} | Width: {width} | Height: {height}', colour=discord.Color.from_rgb(8,12,36))
        embed.set_footer(text="e621", icon_url="https://static.wikia.nocookie.net/logopedia/images/0/0b/Logo_transparent.svg/revision/latest/scale-to-width-down/512?cb=20181119223528")
        embed.set_image(url=image_link)
        await interaction.response.send_message(embed=embed)

        if ext == "webm":
            await interaction.response.send_message(image_link)

client.run('BOT_TOKEN');

