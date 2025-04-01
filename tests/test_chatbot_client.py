import pytest
from chatbot_client.chatbot_client import ChatbotClient


def test_make_request_success(mock_make_request, mock_chatbot_client):
    mock_make_request.return_value = {"success": True}
    response = mock_chatbot_client._make_request("/test")
    assert response == {"success": True}


def test_make_request_failure(mock_make_request, mock_chatbot_client):
    mock_make_request.side_effect = Exception("Request failed")
    with pytest.raises(Exception):
        mock_chatbot_client._make_request("/test")


def test_get_chat_create_response(
    mock_make_request, mock_chatbot_client, chat_create_response_dto
):
    mock_make_request.return_value = chat_create_response_dto.model_dump()
    response = mock_chatbot_client._get_chat_create_reponse()

    assert response.chatId == chat_create_response_dto.chatId
    assert response.botId == chat_create_response_dto.botId
    assert response.botDisplayName == chat_create_response_dto.botDisplayName
    assert response.botDisplayMessage == chat_create_response_dto.botDisplayMessage
    assert response.botDescription == chat_create_response_dto.botDescription


def test_get_chat_response(
    mock_make_request, mock_chatbot_client, get_chat_response_dto
):
    mock_make_request.return_value = get_chat_response_dto.model_dump()
    response = mock_chatbot_client._get_chat_response(chat_id="test_chat_id")

    assert response.chatId == get_chat_response_dto.chatId
    assert response.displayName == get_chat_response_dto.displayName
    assert response.botDisplayName == get_chat_response_dto.botDisplayName


def test_delete_chat(mock_make_request, mock_chatbot_client):
    mock_make_request.return_value = {}
    # Test for successful deletion
    mock_chatbot_client.delete_chat("test_chat_id")
    mock_make_request.assert_called_with(
        endpoint="/api/chats/test_chat_id", method="DELETE"
    )

    # Test for failure and exception
    mock_make_request.side_effect = Exception("Failed to delete chat")
    with pytest.raises(Exception):
        mock_chatbot_client.delete_chat("test_chat_id")


def test_get_chat_completion_response(
    mock_make_request, mock_chatbot_client, chat_completion_response_dto
):
    mock_make_request.return_value = chat_completion_response_dto.model_dump()

    response = mock_chatbot_client._get_chat_completion_response(
        chat_id="test_chat_id",
        user_message="test",
        ignore_chat_history=False,
        is_admin_chat=False,
        is_trace_log_enabled=False,
    )

    assert response == chat_completion_response_dto


def test_create_new_chat_id(
    mock_make_request, mock_chatbot_client, chat_create_response_dto
):
    mock_make_request.return_value = chat_create_response_dto.model_dump()
    chat_id = mock_chatbot_client.create_new_chat_id()

    assert chat_id == chat_create_response_dto.chatId
