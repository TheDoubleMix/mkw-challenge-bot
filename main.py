from typing import Self
from dotenv import load_dotenv
import os
import discord
from discord import app_commands
from discord.ext import commands
from storage import load_chal_num, save_chal_num

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

load_dotenv()

@bot.event
async def on_ready():
    print(f"Bot logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

global chal_num
global common_rules

chal_num = load_chal_num()

common_rules = (
    "## **COMMON RULES:**\n"
    "### **- ANY USE OF TAS/CHEATING IS STRICTLY PROHIBITED**\n"
    "### ** - THE TIME MUST BE SET DURING THE TIME OF THE CHALLENGE BEING HOSTED**\n"
    "### ** - MUST USE ANY OF THE CHARACTERS LISTED ABOVE ⤴️**\n"
)

class View(discord.ui.View):
    def __init__(self, chal_num: int, start_time: str, end_time: str, track: str, characters: str):
        super().__init__()
        self.chal_num = chal_num
        self.track = track
        self.characters = characters
        self.start_time = start_time
        self.end_time = end_time
    
    @discord.ui.button(label="Send Message", style=discord.ButtonStyle.green)
    async def button_callback(self, interaction: discord.Interaction, button: discord.ui.Button[Self]):
        global chal_num
        chal_num += 1
        save_chal_num(chal_num)
        channel = bot.get_channel(1433853482267447407)
        await channel.send((
        f"# **MKWii Challenge #{chal_num+1}:**\n"
        f"Submitted by <@{interaction.user.id}>\n\n"
        f"Begins <t:{self.start_time}:f> and ending <t:{self.end_time}:f>\n"
        "~~---------------------------------------------------~~\n"
        f"## Track: {self.track}\n"
        f"## Characters: {self.characters}\n"
        f"{common_rules}"
        )) # f"## **CHALLENGE-BASED RULES:**"

        for child in self.children:
            if isinstance(child, discord.ui.Button):
                child.disabled = True

        await interaction.response.edit_message(view=self)
        await interaction.followup.send("Message Sent!", ephemeral=True)

@app_commands.describe(
    start_time="The start time in Unix format ( for example 1735670400 ).",
    end_time="The end time in Unix format ( for example 1735843200 ).",
    track="The name the track you want the challenge to be on.",
    characters="The character limitations of the challenge.",
)
@bot.tree.command(name="challenge", description="Hosts a MKWii Challenge.")
async def challenge(interaction: discord.Interaction, start_time: str, end_time: str, track: str, characters: str):
    # TODO: make challenge-based rules and stuff

    await interaction.response.send_message((
        "Preview of message:\n"
        f"# **MKWii Challenge #{chal_num+1}:**\n"
        f"Submitted by <@{interaction.user.id}>\n\n"
        f"Begins <t:{start_time}:f> and ending <t:{end_time}:f>\n"
        "~~---------------------------------------------------~~\n"
        f"## Track: {track}\n"
        f"## Characters: {characters}\n"
        f"{common_rules}"
        ), # f"## **TRACK-BASED RULES:**"
        view=View(chal_num, start_time, end_time, track, characters))
    
    

bot.run(os.getenv("DISCORD_BOT_TOKEN")) # add DISCORD_BOT_TOKEN to your .env file