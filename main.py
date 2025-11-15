from typing import Self
from dotenv import load_dotenv
import os
import discord
from discord import app_commands
from discord.ext import commands
from storage import load_chal_num, save_chal_num, submit_time, load_channel_id, save_channel_id

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
global channel_id

chal_num = load_chal_num()
channel_id = load_channel_id()


common_rules = (
    "## **COMMON RULES:**\n"
    "### **- ANY USE OF TAS/CHEATING IS STRICTLY PROHIBITED**\n"
    "### ** - THE TIME MUST BE SET DURING THE TIME OF THE CHALLENGE BEING HOSTED**\n"
    "### ** - MUST USE ANY OF THE CHARACTERS LISTED ABOVE ⤴️**\n"
)

class View(discord.ui.View):
    def __init__(self, chal_num: int, start_time: str, end_time: str, track: str, characters: str, challenge_rules: str):
        super().__init__()
        self.chal_num = chal_num
        self.start_time = start_time
        self.end_time = end_time
        self.track = track
        self.characters = characters
        self.challenge_rules = challenge_rules

    @discord.ui.button(label="Send Message", style=discord.ButtonStyle.green)
    async def button_callback(self, interaction: discord.Interaction, button: discord.ui.Button[Self]):
        global common_rules
        global chal_num
        chal_num += 1
        save_chal_num(chal_num)
        if channel_id != 0:
            channel = bot.get_channel(channel_id)
        else:
            raise RuntimeError("command 'challenge' ran without channel id being set!")
        await channel.send((
        f"# **MKWii Challenge #{chal_num}:**\n"
        f"Submitted by <@{interaction.user.id}>\n\n"
        f"Begins <t:{self.start_time}:f> and ending <t:{self.end_time}:f>\n"
        "~~---------------------------------------------------~~\n"
        f"## Track: {self.track}\n"
        f"## Characters: {self.characters}\n"
        f"{common_rules}"
        "## **CHALLENGE-BASED RULES:**\n"
        f"{self.challenge_rules}"))

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
    challenge_rules="The rules of the challenge, lines seperated with \"/\"."
)

@bot.tree.command(name="challenge", description="Hosts a MKWii Challenge.")
async def challenge(interaction: discord.Interaction, start_time: str, end_time: str, track: str, characters: str, challenge_rules: str):

    challenge_rules = "- " + challenge_rules.replace("/", "\n- ")

    await interaction.response.send_message((
        "Preview of message:\n"
        f"# **MKWii Challenge #{chal_num+1}:**\n"
        f"Submitted by <@{interaction.user.id}>\n\n"
        f"Begins <t:{start_time}:f> and ending <t:{end_time}:f>\n"
        "~~---------------------------------------------------~~\n"
        f"## Track: {track}\n"
        f"## Characters: {characters}\n"
        f"{common_rules}"
        "## **CHALLENGE-BASED RULES:**\n"
        f"{challenge_rules}"),
        view=View(chal_num, start_time, end_time, track, characters, challenge_rules))
    
@app_commands.describe(
    file="File attachment of the .rkg file"
)

@bot.tree.command(name="submit", description="Submit a time")
async def submit(interaction: discord.Interaction, file: discord.Attachment):

    if channel_id == 0:
        await interaction.response.send_message("The Discord bot is not ready yet.")

    if os.path.splitext(file.filename)[1] != ".rkg":
        await interaction.response.send_message("File needs to be a \".rkg\" file.")
    await interaction.response.send_message(f"<@{interaction.user.id}> Submitted a time!")
    rkg = await file.read()
    time = submit_time(file.filename, rkg)
    await interaction.edit_original_response(content=f"<@{interaction.user.id}> Submitted a time of {time}!")
    
@bot.tree.command(name="setchannel", description="Set the challenge channel for this bot")
async def setchannel(interaction: discord.Interaction):
    await interaction.response.send_message(f"Setting channel id to {interaction.channel.id}", ephemeral=True)
    save_channel_id(interaction.channel.id)
    await interaction.edit_original_response(content=f"Channel id set to {interaction.channel.id}")


bot.run(os.getenv("DISCORD_BOT_TOKEN")) # add DISCORD_BOT_TOKEN to your .env file