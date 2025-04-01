import json
import logging
from typing import Any, Optional

import requests

from chatbot_client.dtos import (
    ChatCompletionRequestDto,
    ChatCompletionResponseDto,
    ChatCreateRequestDto,
    ChatCreateResponseDto,
    GetChatResponseCompletionDto,
    GetChatResponseDto,
    GetOpenChatBotIdResponseDto,
)

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class ChatbotClient:

    def __init__(self, base_url: str, timeout: int = 10):
        self.logger = logger
        self.base_url = base_url
        self.timeout = timeout

    def _make_request(
        self,
        endpoint: str,
        method: str = "GET",
        request_data: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.request(method.upper(), url, json=request_data)
            response.raise_for_status()

            if response.content:
                return response.json()
            return {}
        except requests.exceptions.Timeout:
            raise Exception("Request timed out")
        except requests.exceptions.TooManyRedirects:
            raise Exception("Too many redirects, check the URL")
        except requests.exceptions.RequestException as e:
            raise Exception(f"An error occurred during the request: {e}")
        except Exception as e:
            raise Exception(f"An unexpected error occurred: {e}")

    def _get_open_chat_bot_id_response(self) -> GetOpenChatBotIdResponseDto:
        response = self._make_request("/api/chats/OpenChatBotId")
        open_chat_bot_id = response.get("openChatBotId")
        is_public = response.get("isPublic", False)
        return GetOpenChatBotIdResponseDto(
            openChatBotId=open_chat_bot_id, isPublic=is_public
        )

    def _get_chat_create_reponse(self) -> ChatCreateResponseDto:
        bot_id = self._get_open_chat_bot_id_response().openChatBotId
        request_data = json.loads(ChatCreateRequestDto(botId=bot_id).model_dump_json())
        response = self._make_request(
            endpoint="/api/chats", method="POST", request_data=request_data
        )
        return ChatCreateResponseDto(
            chatId=response.get("chatId"),
            botId=response.get("botId"),
            botDisplayName=response.get("botDisplayName"),
            botDisplayMessage=response.get("botDisplayMessage"),
            botDescription=response.get("botDescription"),
            botSampleQuestion1=response.get("botSampleQuestion1"),
            botSampleQuestion2=response.get("botSampleQuestion2"),
            isUserSystemMessageSupported=response.get(
                "isUserSystemMessageSupported", False
            ),
        )

    def create_new_chat_id(self) -> Optional[str]:
        try:
            response = self._get_chat_create_reponse()
            return response.chatId
        except Exception as e:
            self.logger.warning(f"Failed to create chat - {e}")
            raise

    def delete_chat(self, chat_id: str) -> None:
        try:
            self._make_request(endpoint=f"/api/chats/{chat_id}", method="DELETE")
        except Exception as e:
            self.logger.warning(f"Failed to delete chat with chat_id: {chat_id} - {e}")
            raise

    def _get_chat_completion_response(
        self,
        chat_id: str,
        ignore_chat_history: bool,
        is_admin_chat: bool,
        is_trace_log_enabled: bool,
        user_message: Optional[str] = None,
    ) -> ChatCompletionResponseDto:
        request_data = json.loads(
            ChatCompletionRequestDto(
                userMessage=user_message,
                ignoreChatHistory=ignore_chat_history,
                isAdminChat=is_admin_chat,
                isTraceLogEnabled=is_trace_log_enabled,
            ).model_dump_json()
        )

        response = self._make_request(
            endpoint=f"/api/chats/{chat_id}/completions",
            method="POST",
            request_data=request_data,
        )
        return ChatCompletionResponseDto(
            completionId=response.get("completionId"),
            chatId=response.get("chatId"),
            userMessage=response.get("userMessage"),
            assistantMessage=response.get("assistantMessage"),
            promptTokens=response.get("promptTokens"),
            completionTokens=response.get("completionTokens"),
            totalTokens=response.get("totalTokens"),
            botId=response.get("botId"),
            botDisplayName=response.get("botDisplayName"),
            botDisplayMessage=response.get("botDisplayMessage"),
            botDescription=response.get("botDescription"),
            chatDisplayName=response.get("chatDisplayName"),
            metaData=response.get("metaData"),
            traceLog=response.get("traceLog"),
        )

    def send_and_receive_message_to_chat(
        self,
        chat_id: str,
        user_message: Optional[str],
        ignore_chat_history: bool,
        is_admin_chat: bool,
        is_trace_log_enabled: bool,
    ) -> Optional[str]:
        try:
            response = self._get_chat_completion_response(
                chat_id=chat_id,
                user_message=user_message,
                ignore_chat_history=ignore_chat_history,
                is_admin_chat=is_admin_chat,
                is_trace_log_enabled=is_trace_log_enabled,
            )
            self.logger.info(
                f"Succesfully sent and received message to chat with chat_id: {chat_id}"
            )
            return response.assistantMessage
        except Exception as e:
            self.logger.warning(
                f"Failed to send message to chat with chat_id: {chat_id} - {e}"
            )
            raise

    def _get_chat_response(self, chat_id: str) -> GetChatResponseDto:
        response = self._make_request(endpoint=f"/api/chats/{chat_id}")
        return GetChatResponseDto(
            chatId=response.get("chatId"),
            displayName=response.get("displayName"),
            createdUtc=response.get("createdUtc"),
            lastAccessedUtc=response.get("lastAccessedUtc"),
            botId=response.get("botId"),
            botDisplayName=response.get("botDisplayName"),
            botDisplayMessage=response.get("botDisplayMessage"),
            botDescription=response.get("botDescription"),
            botSampleQuestion1=response.get("botSampleQuestion1"),
            botSampleQuestion2=response.get("botSampleQuestion2"),
            completions=[
                GetChatResponseCompletionDto(**comp)
                for comp in response.get("completions", [])
            ],  # Mock
            isFavorite=response.get("isFavorite"),
            isUserSystemMessageSupported=response.get("isUserSystemMessageSupported"),
            userSystemMessageId=response.get("userSystemMessageId"),
            userSystemMessageDisplayName=response.get("userSystemMessageDisplayName"),
        )

    def get_existing_chat(self, chat_id: str) -> Optional[str]:
        try:
            response = self._get_chat_response(chat_id=chat_id)
            return response.chatId
        except Exception as e:
            self.logger.warning(f"Failed to fetch chat with chat_id: {chat_id} - {e}")
            raise
