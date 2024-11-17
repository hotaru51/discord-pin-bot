# -*- coding: utf-8 -*-
import logging

import discord


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class PinBot(discord.Client):
    """メッセージに特定のリアクションがついたものをピン留めするBotクラス
    """

    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        """メッセージにリアクションが付いた時に実行される

        Args:
            payload (discord.RawReactionActionEvent): リアクション追加時のイベント
        """

        logger.info(str(payload))

    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        """メッセージのリアクションが削除された時に実行される

        Args:
            payload (discord.RawReactionClearEvent): リアクション削除時のイベント
        """

        logger.info(str(payload))
