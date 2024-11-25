# -*- coding: utf-8 -*-
import os
import sys
import logging
import signal
import asyncio
import functools

import discord

import bot


def handler(client: bot.PinBot, signal, frame):
    """bot停止用のハンドラ

    Args:
        client (bot.PinBot): PinBotインスタンス
        signal: シグナル
        frame: フレームオブジェクト
    """

    asyncio.get_event_loop().create_task(client.close())


logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

DISCORD_TOKEN = os.environ.get('PIN_BOT_TOKEN')

if DISCORD_TOKEN is None:
    logging.error('Environment variable PIN_BOT_TOKEN is undefined.')
    sys.exit(1)

client = bot.PinBot(intents=discord.Intents.default())

# SIGTERM、SIGINTを受け取ったときにcloseする
h = functools.partial(handler, client)
signal.signal(signal.SIGTERM, h)
signal.signal(signal.SIGINT, h)

client.run(token=DISCORD_TOKEN)
