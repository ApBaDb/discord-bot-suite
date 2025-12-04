import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncio
import random

# ------------------ CONFIG ------------------
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ------------------ EVENTS ------------------
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

# ------------------ AUTOMATION ------------------
@bot.command()
async def remind(ctx, seconds: int, *, task: str):
    """Set a reminder: !remind <seconds> <task>"""
    await ctx.send(f"⏳ Reminder set for {seconds} seconds: {task}")
    await asyncio.sleep(seconds)
    await ctx.send(f"🔔 Reminder: {task}")

# ------------------ MODERATION ------------------
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="No reason provided"):
    await member.kick(reason=reason)
    await ctx.send(f"👢 {member} was kicked. Reason: {reason}")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="No reason provided"):
    await member.ban(reason=reason)
    await ctx.send(f"⛔ {member} was banned. Reason: {reason}")

# ------------------ LOGGING ------------------
@bot.event
async def on_message_delete(message):
    if message.author.bot:
        return
    log_channel = discord.utils.get(message.guild.text_channels, name="logs")
    if log_channel:
        await log_channel.send(
            f"🗑️ Message deleted in {message.channel.mention} by {message.author}: {message.content}"
        )

# ------------------ PERMISSIONS ------------------
@bot.command()
async def secret(ctx):
    """Staff-only command"""
    if not discord.utils.get(ctx.author.roles, name="Staff"):
        return await ctx.send("🚫 You don’t have permission!")
    await ctx.send("✅ Staff-only command executed.")

# ------------------ CUSTOM COMMANDS ------------------
@bot.command()
async def hello(ctx):
    await ctx.send(f"👋 Hello {ctx.author.mention}, I’m your custom bot!")

# ------------------ MUSIC (placeholder) ------------------
@bot.command()
async def play(ctx, *, song: str):
    await ctx.send(f"🎵 Pretending to play: {song}")
    # Real music requires FFmpeg/Lavalink setup

# ------------------ GAMES ------------------
@bot.command()
async def dice(ctx):
    roll = random.randint(1, 6)
    await ctx.send(f"🎲 You rolled a {roll}!")

# ------------------ RUN ------------------
bot.run(TOKEN)
