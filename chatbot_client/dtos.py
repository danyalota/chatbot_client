from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class GetOpenChatBotIdResponseDto(BaseModel):
    openChatBotId: Optional[str] = None
    isPublic: bool


class ChatCreateRequestDto(BaseModel):
    botId: Optional[str] = None


class ChatCreateResponseDto(BaseModel):
    chatId: Optional[str] = None
    botId: Optional[str] = None
    botDisplayName: Optional[str] = None
    botDisplayMessage: Optional[str] = None
    botDescription: Optional[str] = None
    botSampleQuestion1: Optional[str] = None
    botSampleQuestion2: Optional[str] = None
    isUserSystemMessageSupported: bool


class ChatCompletionRequestDto(BaseModel):
    userMessage: Optional[str] = None
    ignoreChatHistory: bool
    isAdminChat: bool
    isTraceLogEnabled: bool


class ChatCompletionResponseDto(BaseModel):
    completionId: Optional[str] = None
    chatId: Optional[str] = None
    userMessage: Optional[str] = None
    assistantMessage: Optional[str] = None
    promptTokens: Optional[int] = None
    completionTokens: Optional[int] = None
    totalTokens: Optional[int] = None
    botId: Optional[str] = None
    botDisplayName: Optional[str] = None
    botDisplayMessage: Optional[str] = None
    botDescription: Optional[str] = None
    chatDisplayName: Optional[str] = None
    metaData: Optional[dict] = None
    traceLog: Optional[str] = None


# Mocked
class GetChatResponseCompletionDto(BaseModel):
    pass


class GetChatResponseDto(BaseModel):
    chatId: Optional[str] = None
    displayName: Optional[str] = None
    createdUtc: Optional[datetime] = None
    lastAccessedUtc: Optional[datetime] = None
    botId: Optional[str] = None
    botDisplayName: Optional[str] = None
    botDisplayMessage: Optional[str] = None
    botDescription: Optional[str] = None
    botSampleQuestion1: Optional[str] = None
    botSampleQuestion2: Optional[str] = None
    completions: Optional[list[GetChatResponseCompletionDto]] = None
    isFavorite: Optional[bool] = None
    isUserSystemMessageSupported: Optional[bool] = None
    userSystemMessageId: Optional[str] = None
    userSystemMessageDisplayName: Optional[str] = None
