from unittest.mock import patch

import pytest

from chatbot_client.chatbot_client import ChatbotClient
from chatbot_client.dtos import (
    ChatCompletionRequestDto,
    ChatCompletionResponseDto,
    ChatCreateRequestDto,
    ChatCreateResponseDto,
    GetChatResponseCompletionDto,
    GetChatResponseDto,
    GetOpenChatBotIdResponseDto,
)


# Fixtures for DTOs
@pytest.fixture
def chat_create_request_dto():
    return ChatCreateRequestDto(botId="test_bot_id")


@pytest.fixture
def chat_create_response_dto():
    return ChatCreateResponseDto(
        chatId="test_chat_id",
        botId="test_bot_id",
        botDisplayName="Test Bot",
        botDisplayMessage="How can I assist you?",
        botDescription="A chatbot for test purposes",
        botSampleQuestion1="What's your name?",
        botSampleQuestion2="How are you?",
        isUserSystemMessageSupported=True,
    )


@pytest.fixture
def chat_completion_request_dto():
    return ChatCompletionRequestDto(
        userMessage="Hello",
        ignoreChatHistory=False,
        isAdminChat=False,
        isTraceLogEnabled=False,
    )


@pytest.fixture
def get_chat_response_dto():
    return GetChatResponseDto(
        chatId="test_chat_id",
        displayName="Test Chat",
        createdUtc="2025-01-01T00:00:00Z",
        lastAccessedUtc="2025-01-02T00:00:00Z",
        botId="test_bot_id",
        botDisplayName="Test Bot",
        botDisplayMessage="How can I assist you?",
        botDescription="A chatbot for test purposes",
        botSampleQuestion1="What's your name?",
        botSampleQuestion2="How are you?",
        completions=[
            GetChatResponseCompletionDto(completionId="1234", message="Hello")
        ],
        isFavorite=False,
        isUserSystemMessageSupported=True,
        userSystemMessageId="sys_msg_1",
        userSystemMessageDisplayName="System Message",
    )


@pytest.fixture
def chat_completion_response_dto():
    return ChatCompletionResponseDto(
        completionId="12345",
        chatId="67890",
        userMessage="Hello, chatbot!",
        assistantMessage="Hello, how can I assist you?",
        promptTokens=10,
        completionTokens=20,
        totalTokens=30,
        botId="bot-123",
        botDisplayName="Chatbot",
        botDisplayMessage="Welcome to our chatbot!",
        botDescription="A helpful AI chatbot",
        chatDisplayName="User Chat",
        metaData={"key": "value"},
        traceLog="Trace log data",
    )


@pytest.fixture
def open_chat_bot_id_response_dto():
    return GetOpenChatBotIdResponseDto(openChatBotId="test_bot_id", isPublic=False)


# Mock make_request function
@pytest.fixture
def mock_make_request():
    with patch.object(ChatbotClient, "_make_request") as mock:
        yield mock


@pytest.fixture
def mock_chatbot_client():
    client = ChatbotClient(base_url="http://fakeurl.com")
    return client
