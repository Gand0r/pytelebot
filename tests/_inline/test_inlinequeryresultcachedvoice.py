#!/usr/bin/env python
#
# A library that provides a Python interface to the Telegram Bot API
# Copyright (C) 2015-2025
# Leandro Toledo de Souza <devs@python-telegram-bot.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser Public License for more details.
#
# You should have received a copy of the GNU Lesser Public License
# along with this program.  If not, see [http://www.gnu.org/licenses/].
import pytest

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultCachedAudio,
    InlineQueryResultCachedVoice,
    InputTextMessageContent,
    MessageEntity,
)
from tests.auxil.slots import mro_slots


@pytest.fixture(scope="module")
def inline_query_result_cached_voice():
    return InlineQueryResultCachedVoice(
        InlineQueryResultCachedVoiceTestBase.id_,
        InlineQueryResultCachedVoiceTestBase.voice_file_id,
        InlineQueryResultCachedVoiceTestBase.title,
        caption=InlineQueryResultCachedVoiceTestBase.caption,
        parse_mode=InlineQueryResultCachedVoiceTestBase.parse_mode,
        caption_entities=InlineQueryResultCachedVoiceTestBase.caption_entities,
        input_message_content=InlineQueryResultCachedVoiceTestBase.input_message_content,
        reply_markup=InlineQueryResultCachedVoiceTestBase.reply_markup,
    )


class InlineQueryResultCachedVoiceTestBase:
    id_ = "id"
    type_ = "voice"
    voice_file_id = "voice file id"
    title = "title"
    caption = "caption"
    parse_mode = "HTML"
    caption_entities = [MessageEntity(MessageEntity.ITALIC, 0, 7)]
    input_message_content = InputTextMessageContent("input_message_content")
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("reply_markup")]])


class TestInlineQueryResultCachedVoiceWithoutRequest(InlineQueryResultCachedVoiceTestBase):
    def test_slot_behaviour(self, inline_query_result_cached_voice):
        inst = inline_query_result_cached_voice
        for attr in inst.__slots__:
            assert getattr(inst, attr, "err") != "err", f"got extra slot '{attr}'"
        assert len(mro_slots(inst)) == len(set(mro_slots(inst))), "duplicate slot"

    def test_expected_values(self, inline_query_result_cached_voice):
        assert inline_query_result_cached_voice.type == self.type_
        assert inline_query_result_cached_voice.id == self.id_
        assert inline_query_result_cached_voice.voice_file_id == self.voice_file_id
        assert inline_query_result_cached_voice.title == self.title
        assert inline_query_result_cached_voice.caption == self.caption
        assert inline_query_result_cached_voice.parse_mode == self.parse_mode
        assert inline_query_result_cached_voice.caption_entities == tuple(self.caption_entities)
        assert (
            inline_query_result_cached_voice.input_message_content.to_dict()
            == self.input_message_content.to_dict()
        )
        assert (
            inline_query_result_cached_voice.reply_markup.to_dict() == self.reply_markup.to_dict()
        )

    def test_caption_entities_always_tuple(self):
        result = InlineQueryResultCachedVoice(self.id_, self.voice_file_id, self.title)
        assert result.caption_entities == ()

    def test_to_dict(self, inline_query_result_cached_voice):
        inline_query_result_cached_voice_dict = inline_query_result_cached_voice.to_dict()

        assert isinstance(inline_query_result_cached_voice_dict, dict)
        assert (
            inline_query_result_cached_voice_dict["type"] == inline_query_result_cached_voice.type
        )
        assert inline_query_result_cached_voice_dict["id"] == inline_query_result_cached_voice.id
        assert (
            inline_query_result_cached_voice_dict["voice_file_id"]
            == inline_query_result_cached_voice.voice_file_id
        )
        assert (
            inline_query_result_cached_voice_dict["title"]
            == inline_query_result_cached_voice.title
        )
        assert (
            inline_query_result_cached_voice_dict["caption"]
            == inline_query_result_cached_voice.caption
        )
        assert (
            inline_query_result_cached_voice_dict["parse_mode"]
            == inline_query_result_cached_voice.parse_mode
        )
        assert inline_query_result_cached_voice_dict["caption_entities"] == [
            ce.to_dict() for ce in inline_query_result_cached_voice.caption_entities
        ]
        assert (
            inline_query_result_cached_voice_dict["input_message_content"]
            == inline_query_result_cached_voice.input_message_content.to_dict()
        )
        assert (
            inline_query_result_cached_voice_dict["reply_markup"]
            == inline_query_result_cached_voice.reply_markup.to_dict()
        )

    def test_equality(self):
        a = InlineQueryResultCachedVoice(self.id_, self.voice_file_id, self.title)
        b = InlineQueryResultCachedVoice(self.id_, self.voice_file_id, self.title)
        c = InlineQueryResultCachedVoice(self.id_, "", self.title)
        d = InlineQueryResultCachedVoice("", self.voice_file_id, self.title)
        e = InlineQueryResultCachedAudio(self.id_, "", "")

        assert a == b
        assert hash(a) == hash(b)
        assert a is not b

        assert a == c
        assert hash(a) == hash(c)

        assert a != d
        assert hash(a) != hash(d)

        assert a != e
        assert hash(a) != hash(e)
