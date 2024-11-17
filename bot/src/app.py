# -*- coding: utf-8 -*-
import os
import sys
import logging

import discord

import bot


logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

DISCORD_TOKEN = os.environ.get('PIN_BOT_TOKEN')

if DISCORD_TOKEN is None:
    logging.error('Environment variable PIN_BOT_TOKEN is undefined.')
    sys.exit(1)

client = bot.PinBot(intents=discord.Intents.default())
client.run(token=DISCORD_TOKEN)
