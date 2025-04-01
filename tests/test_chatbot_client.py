import pytest
from unittest.mock import MagicMock


def test_make_request(mock_chatbot_client):
    mock_chatbot_client._make_request = MagicMock(return_value={"success": True})
    response = mock_chatbot_client._make_request("/test")
    assert response == {"success": True}

    mock_chatbot_client._make_request = MagicMock(
        side_effect=Exception("Request failed")
    )
    with pytest.raises(Exception):
        mock_chatbot_client._make_request("/test")


def test_get_open_chat_bot_id_response(
    mock_chatbot_client, open_chat_bot_id_response_dto
):
    mock_chatbot_client._make_request = MagicMock(
        return_value={
            "openChatBotId": open_chat_bot_id_response_dto.openChatBotId,
            "isPublic": open_chat_bot_id_response_dto.isPublic,
        }
    )
    response = mock_chatbot_client._get_open_chat_bot_id_response()
    assert response.openChatBotId == open_chat_bot_id_response_dto.openChatBotId
    assert response.isPublic == open_chat_bot_id_response_dto.isPublic


def test_get_chat_create_response(mock_chatbot_client, chat_create_response_dto):
    mock_chatbot_client._make_request = MagicMock(
        return_value=chat_create_response_dto.model_dump()
    )
    response = mock_chatbot_client._get_chat_create_reponse()

    assert response.chatId == chat_create_response_dto.chatId
    assert response.botId == chat_create_response_dto.botId
    assert response.botDisplayName == chat_create_response_dto.botDisplayName
    assert response.botDisplayMessage == chat_create_response_dto.botDisplayMessage
    assert response.botDescription == chat_create_response_dto.botDescription


def test_create_new_chat_id(mock_chatbot_client, chat_create_response_dto):
    mock_chatbot_client._make_request = MagicMock(
        return_value=chat_create_response_dto.model_dump()
    )
    chat_id = mock_chatbot_client.create_new_chat_id()
    assert chat_id == chat_create_response_dto.chatId

    # Test for failure and exception
    mock_chatbot_client._make_request.side_effect = Exception("Error occured")
    mock_chatbot_client.logger = MagicMock()

    with pytest.raises(Exception):
        mock_chatbot_client.create_new_chat_id()

    mock_chatbot_client.logger.warning.assert_called_with(
        "Failed to create chat - Error occured"
    )


def test_delete_chat(mock_chatbot_client):
    mock_chatbot_client._make_request = MagicMock(return_value={})
    mock_chatbot_client.delete_chat("test_chat_id")
    mock_chatbot_client._make_request.assert_called_with(
        endpoint="/api/chats/test_chat_id", method="DELETE"
    )

    # Test for failure and exception
    mock_chatbot_client._make_request.side_effect = Exception("Error occured")
    mock_chatbot_client.logger = MagicMock()

    with pytest.raises(Exception):
        mock_chatbot_client.delete_chat("test_chat_id")

    mock_chatbot_client.logger.warning.assert_called_with(
        "Failed to delete chat with chat_id: test_chat_id - Error occured"
    )


def test_get_chat_completion_response(
    mock_chatbot_client, chat_completion_response_dto
):
    mock_chatbot_client._make_request = MagicMock(
        return_value=chat_completion_response_dto.model_dump()
    )

    response = mock_chatbot_client._get_chat_completion_response(
        chat_id="test_chat_id",
        user_message="test",
        ignore_chat_history=False,
        is_admin_chat=False,
        is_trace_log_enabled=False,
    )

    assert response == chat_completion_response_dto


def test_send_and_receive_message_to_chat(
    mock_chatbot_client, chat_completion_response_dto
):
    mock_chatbot_client._get_chat_completion_response = MagicMock(
        return_value=chat_completion_response_dto
    )
    assistant_message = mock_chatbot_client.send_and_receive_message_to_chat(
        chat_id="test_chat_id",
        user_message="Hello!",
        ignore_chat_history=False,
        is_admin_chat=False,
        is_trace_log_enabled=False,
    )
    assert assistant_message == chat_completion_response_dto.assistantMessage

    # Test for failure and exception
    mock_chatbot_client._get_chat_completion_response.side_effect = Exception(
        "Error occurred"
    )
    mock_chatbot_client.logger = MagicMock()

    with pytest.raises(Exception):
        mock_chatbot_client.send_and_receive_message_to_chat(
            chat_id="test_chat_id",
            user_message="Hello!",
            ignore_chat_history=False,
            is_admin_chat=False,
            is_trace_log_enabled=False,
        )
    mock_chatbot_client.logger.warning.assert_called_with(
        "Failed to send message to chat with chat_id: test_chat_id - Error occurred"
    )


def test_get_chat_response(mock_chatbot_client, get_chat_response_dto):
    mock_chatbot_client._make_request = MagicMock(
        return_value=get_chat_response_dto.model_dump()
    )
    response = mock_chatbot_client._get_chat_response(chat_id="test_chat_id")

    assert response.chatId == get_chat_response_dto.chatId
    assert response.displayName == get_chat_response_dto.displayName
    assert response.botDisplayName == get_chat_response_dto.botDisplayName


def test_get_existing_chat(mock_chatbot_client, get_chat_response_dto):
    mock_chatbot_client._get_chat_response = MagicMock(
        return_value=get_chat_response_dto
    )

    chat_id = mock_chatbot_client.get_existing_chat("test_chat_id")
    assert chat_id == get_chat_response_dto.chatId

    # Test for failure and exception
    mock_chatbot_client._get_chat_response.side_effect = Exception("Error occurred")
    mock_chatbot_client.logger = MagicMock()

    with pytest.raises(Exception):
        mock_chatbot_client.get_existing_chat("test_chat_id")

    mock_chatbot_client.logger.warning.assert_called_with(
        "Failed to fetch chat with chat_id: test_chat_id - Error occurred"
    )
