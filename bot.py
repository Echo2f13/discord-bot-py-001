import random
import discord
import os
from discord.ext import commands
# google-api-python-client library, grtting build class
from googleapiclient.discovery import build

# Instaloader and instagram_private_api to download the Instagram post
import instaloader
from instagram_private_api import Client, ClientCompatPatch

# async-io is for proper scheduling for new pulls
import asyncio

# using imgurpython to generate url form local images
from imgurpython import ImgurClient
# client = ImgurClient('YOUR_CLIENT_ID', 'YOUR_CLIENT_SECRET')
client = ImgurClient(
    'a86891a3cfcd974', '9779240dc03e5512903679ada9d6d158c128f15f')


# imported discord module
# from discord.ext brought out the commands.

intents = discord.Intents.all()
# intnts.members = True
# intnts.message_content = True

# introducing new veriable for client input "c"
c_bot = commands.Bot(command_prefix='$', intents=intents)
# c_bot = discord.Client()
# commands.Bot will envoke the bot and command_prefix is the the command that we have to use to envoke the bot.


# introducing new veriable for client input "insta_loader "
insta_loader = instaloader.Instaloader()
print("insta_loader is on the work")

# apikey of google images
api_key = 'AIzaSyDT88ZeDKlcoCtdo9xl8U3dgAC2PdxUF1o'
print("api key is running")

# creating events that bot needs to perform
# when_ready is a async function which will be triggered once the bot is running. [agenda of the the when_ready function]


def upload_image_to_imgur(image_path):
    print("upload_image_to_imgur")
    try:
        print("entered TRY")
        print("Image Path:", image_path)
        # Upload the image to Imgur
        uploaded_image = client.upload_from_path(image_path, anon=True)
        print("Uploaded image", uploaded_image)

        # Get the URL of the uploaded image
        image_url = uploaded_image['link']
        print("image_url:", image_url)
        return image_url

    except Exception as e:
        print("entered exception")
        print(f"Error uploading image: {e}")
        return None


async def check_instagram_post():
    print("check_instagram_post function triggered")
    try:
        print("entered try")
        profile = instaloader.Profile.from_username(
            insta_loader.context, 'heehee4_23')
        print(profile.username)

        # post = profile.get_posts()[0]  # Gets the most recent post
        post = next(profile.get_posts(), None)
        print(post)

        # Download the post image
        insta_loader.download_post(post, target=profile.username)
        print("downloading the post is completed")

        with open(f'{profile.username}/{post.date_utc.strftime("%Y-%m-%d_%H-%M-%S")}_UTC_1.jpg', 'rb') or open(f'{profile.username}/{post.date_utc.strftime("%Y-%m-%d_%H-%M-%S")}_UTC.jpg', 'rb') as f:
            if open(f'{profile.username}/{post.date_utc.strftime("%Y-%m-%d_%H-%M-%S")}_UTC_1.jpg', 'rb'):
                with open(f'{profile.username}/{post.date_utc.strftime("%Y-%m-%d_%H-%M-%S")}_UTC_2.jpg', 'rb') as f1:
                    print("opening downloaded picture on discord entered")
                    print("Picture:", f.name)
                    print("Picture:", f1.name)
                    image_url = upload_image_to_imgur(f.name)
                    image_url_2 = upload_image_to_imgur(f1.name)
                    print("image URL:", image_url)
                    print("image URL:", image_url_2)
                    if (image_url and image_url_2) != None:
                        print(f"Image URL: {image_url}")
                        print(f"Image URL: {image_url_2}")
                        # picture = discord.File(f)
                        # print("actual picture:", picture)
                        # await ctx.channel.send(file=picture)
                        embed1 = discord.Embed(
                            title="Instagram Post", description="no discription for now", color=0x00ff00)

                        # file = discord.File(f, filename="image.png")
                        embed1.add_field(
                            name="Image 1", value="No post description yet", inline=False)
                        embed1.set_image(url=image_url)
                        embed1.set_image(url=image_url_2)

                        # file = discord.File(picture)
                        # e = discord.Embed()
                        # e.set_image(url="attachment://output.png")
                        # await ctx.send(file=file, embed=e)

                        # Send the post URL to Discord
                        # channel = bot.get_channel(YOUR_DISCORD_CHANNEL_ID)  # Replace with the actual Discord channel ID
                        channel = c_bot.get_channel(838679509829419011)

                        # embed1.set_image(file=picture)
                        await channel.send(embed=embed1)
                        print("opening downloaded picture on discord ended properly")
                    else:
                        print("Image upload failed.")
                        channel = c_bot.get_channel(838679509829419011)

                        # embed1.set_image(file=picture)
                        await channel.send("error")
                        print(
                            "opening downloaded picture on discord ended without req")
            else:
                print("opening downloaded picture on discord entered")
                print("Picture:", f.name)
                image_url = upload_image_to_imgur(f.name)
                print("image URL:", image_url)
                if image_url != None:
                    print(f"Image URL: {image_url}")
                    # picture = discord.File(f)
                    # print("actual picture:", picture)
                    # await ctx.channel.send(file=picture)
                    embed1 = discord.Embed(
                        title="Instagram Post", description="no discription for now", color=0x00ff00)

                    # file = discord.File(f, filename="image.png")
                    embed1.set_image(url=image_url)

                    # file = discord.File(picture)
                    # e = discord.Embed()
                    # e.set_image(url="attachment://output.png")
                    # await ctx.send(file=file, embed=e)

                    # Send the post URL to Discord
                    # channel = bot.get_channel(YOUR_DISCORD_CHANNEL_ID)  # Replace with the actual Discord channel ID
                    channel = c_bot.get_channel(838679509829419011)

                    # embed1.set_image(file=picture)
                    await channel.send(embed=embed1)
                    print("opening downloaded picture on discord ended properly")
                else:
                    print("Image upload failed.")
                    channel = c_bot.get_channel(838679509829419011)

                    # embed1.set_image(file=picture)
                    await channel.send("error")
                    print("opening downloaded picture on discord ended without req")
    except Exception as e:
        print("entered exception")
        await c_bot.channel.send(f"Error: {e}")
        print("Error:", e)
        print("entered exception ended")


async def poll_instagram():
    while True:
        print("entered scheduling check for the new post")
        await check_instagram_post()
        path = r'C:\impfolder\study sftwr\projects\Discord bot\theotakuclub_vit'
        print("path:", path)
        try:
            os.rmdir(path)
            print(path, " deleted")
        except Exception as e:
            print("not deleted the ", path)
        print("entered scheduling check for the new post ended and sleeping for 5min(300s)")
        await asyncio.sleep(300)  # Poll every 300 seconds (adjust as needed)


@c_bot.event
async def on_ready():
    print("pass 1")
    print(f'Logged in as {c_bot.user} (ID: {c_bot.user.id})')
    print("pass 1 emd")
    c_bot.loop.create_task(poll_instagram())

target_role_id = 1121347680921194496
target_message_id = 1134002692893712394


@c_bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id == target_message_id:
        guild = c_bot.get_guild(payload.guild_id)
        role = guild.get_role(target_role_id)
        member = guild.get_member(payload.user_id)
        await member.add_roles(role)


@c_bot.event
async def on_raw_reaction_remove(payload):
    if payload.message_id == target_message_id:
        guild = c_bot.get_guild(payload.guild_id)
        role = guild.get_role(target_role_id)
        member = guild.get_member(payload.user_id)
        await member.remove_roles(role)


# @c.event
# async def on_message(ctx):
#     if ctx.author == c.user:
#         print("message author :", c.user)
#         return

#     if ctx.content.startswith('!get_insta_post'):
#         print("!get_insta_post is triggered but done nothing")
#         try:
#             # Replace 'instagram_username' with the username of the Instagram account
#             # profile = instaloader.Profile.from_username(insta_loader.context, 'instagram_username')
#             profile = instaloader.Profile.from_username(
#                 insta_loader.context, 'trendy.manga')
#             print(profile.username)
#             # post = profile.get_posts()[0]  # Gets the most recent post
#             post = next(profile.get_posts(), None)

#             print(post)

#             # Download the post image
#             insta_loader.download_post(post, target=profile.username)
#             print("downloading the post is completed")

#             # Send the post image to Discord
#             with open(f'{profile.username}/{post.date_utc.strftime("%Y-%m-%d_%H-%M-%S")}_UTC.jpg', 'rb') as f:
#                 print("opening downloaded picture on discord entered")
#                 print("Picture:", f)
#                 picture = discord.File(f)
#                 print("actual picture:", picture)
#                 # await ctx.channel.send(file=picture)
#                 embed1 = discord.Embed(
#                     title="Instagram Post", description="Desc", color=0x00ff00)
#                 # file = discord.File(f, filename="image.png")
#                 embed1.set_image(url=f)

#                 # file = discord.File(picture)
#                 # e = discord.Embed()
#                 # e.set_image(url="attachment://output.png")
#                 # await ctx.send(file=file, embed=e)

#                 # embed1.set_image(file=picture)
#                 await ctx.channel.send(embed=embed1)
#                 print("opening downloaded picture on discord ended")

    # except Exception as e:
    #     print("entered exception")
    #     await ctx.channel.send(f"Error: {e}")
    #     print("Error:", e)
    #     print("entered exception ended")


@c_bot.command()
async def bothelp(ctx):
    print("pass help asked")
    embededtext = discord.Embed(
        title='prefix *$* \n3 main commands \n$search <search> \n   (this search any image)\nclear')
    await ctx.send(embed=embededtext)
    print("pass help asked end")
    # await ctx.send('prefix *$* \n3 main commands \n-ass\nboobs\nshow <search> \n   (this search any image)\nclear')


# command for google image search, with sh
@c_bot.command(aliases=["search"])
async def showpic(ctx, *, search):
    print("pass show pic")
    r = random.randint(0, 9)
    resource = build("customsearch", "v1", developerKey=api_key).cse()
    result = resource.list(
        q=f"{search}", cx="a0039021d66464b64", searchType="image"
    ).execute()
    url = result["items"][r]["link"]
    embed1 = discord.Embed()
    embed1.set_image(url=url)
    await ctx.send(embed=embed1)
    print("pass show pic end")

# command to clear text


@c_bot.command()
async def clear(ctx, amount=10):
    print("pass clear")
    await ctx.channel.purge(limit=amount)
    print("pass clear end")


# to run the event
c_bot.run('MTEzMjM3ODQ3NzQwMDcwNzA3Mg.GUH-HB.nwjlsIFHhXrt_ltN0GULgUL20_tBQ6KU_ln4r4')
# the token of the bot is placed in the clients event run as a string
