# -*- coding: utf-8 -*-
import logging
import json

import discord


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

TARGET_REACTION = 'pin_dome'


class PinBot(discord.Client):
    """メッセージに特定のリアクションがついたものをピン留めするBotクラス"""

    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        """メッセージにリアクションが付いた時に実行される

        Args:
            payload (discord.RawReactionActionEvent): リアクション追加時のイベント
        """

        logger.info(payload)

        if payload.emoji.name != TARGET_REACTION:
            logger.info('do nothing.')
            return

        state = PinState(payload, self)
        await state.fetch()
        logger.info(state)

        if not state.is_pinned():
            await state.pin()
        else:
            logger.info('already pinned.')

    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        """メッセージのリアクションが削除された時に実行される

        Args:
            payload (discord.RawReactionClearEvent): リアクション削除時のイベント
        """

        logger.info(payload)

        if payload.emoji.name != TARGET_REACTION:
            logger.info('do nothing.')
            return

        state = PinState(payload, self)
        await state.fetch()
        logger.info(state)

        if state.is_pinned():
            await state.unpin()
        else:
            logger.info('not pinned.')

        if TARGET_REACTION in state.existing_reactions:
            await state.clear_reaction()


class PinState():
    """メッセージのリアクションイベントからピン留めの状態を取得、操作するクラス

    Attributes:
        client (PinBot): PinBotインスタンス
        event (discord.RawReactionActionEvent): リアクション追加/削除時のイベント
        reaction (str): 追加/削除されたリアクションのemoji名
        message (Optional[discord.Message]): 対象のメッセージ fetch実行前はNone
        existing_reactions (list[str]): イベント発生後のメッセージのリアクション一覧 fetch実行前は空のリスト
    """

    def __init__(self, event: discord.RawReactionActionEvent, client: PinBot):
        """PinStateのインスタンスを生成

        リアクションのイベントから対象メッセージ、ピン留めの状態を取得する

        Args:
            event (discord.RawReactionActionEvent): リアクションのイベント
        """
        self.client = client
        self.event = event
        self.reaction = self.event.emoji.name
        self.message: discord.Message | None = None
        self.existing_reactions: list[str] = []

    async def fetch(self):
        """対象メッセージのデータを取得する"""

        channel_id = self.event.channel_id
        message_id = self.event.message_id

        logger.info('fetch target message. (channel_id: {}, message_id: {})'.format(
            channel_id, message_id))
        self.message = await self.client.get_partial_messageable(
            self.event.channel_id
        ).fetch_message(self.event.message_id)

        # イベント発生後のリアクションの一覧取得
        for r in self.message.reactions:
            if isinstance(r.emoji, discord.PartialEmoji) or isinstance(r.emoji, discord.Emoji):
                self.existing_reactions.append(r.emoji.name)
            else:
                self.existing_reactions.append(r.emoji)

    def is_pinned(self) -> bool:
        """ピン留め済みか確認する

        Returns:
            bool: ピン留め済みならTrue(fetch()実行前は状態に関わらずFalse)
        """

        if self.message is None:
            return False

        return self.message.pinned

    async def pin(self):
        """メッセージをピン留めする"""

        if self.message is not None:
            logger.info('pin message. (message_id: {})'.format(self.message.id))
            await self.message.pin()

    async def unpin(self):
        """メッセージのピン留めを解除する"""

        if self.message is not None:
            logger.info('unpin message. (message_id: {})'.format(self.message.id))
            await self.message.unpin()

    async def clear_reaction(self):
        """リアクションを削除する"""

        if self.message is not None:
            logger.info('clear target reactions.')
            await self.message.clear_reaction(self.event.emoji)

    def __str__(self) -> str:
        """ステータスを文字列にJSON整形して返す"""

        res = {
            'event_type': self.event.event_type,
            'reaction': self.reaction,
            'is_pinned': self.is_pinned(),
            'existing_reactions': self.existing_reactions
        }

        return json.dumps(res)
