# Chatbot Client

### Installing the Module

Clone the repository and navigate into the project directory:

```bash
$ git clone https://github.com/danyalota/chatbot_client.git
$ cd chatbot_client
```

Install the required dependencies:

```bash
$ pip install .
```

## Usage

### Importing and Initializing the Chatbot Client

```python
from chatbot_client.chatbot import ChatbotClient

base_url = "https://api.example.com"  # Replace with the actual API base URL
client = ChatbotClient(base_url=base_url)
```

### Creating a New Chat

```python
chat_id = client.create_new_chat_id()
```

### Sending a Message and receiving a response

```python
response = client.send_message_to_chat(
    chat_id=chat_id,
    user_message="Hello, chatbot!",
    ignore_chat_history=False,
    is_admin_chat=False,
    is_trace_log_enabled=False
)
```

### Fetching Data of an Existing Chat

```python
chat_data = client.get_existing_chat(chat_id)
```

### Deleting a Chat

```python
client.delete_chat(chat_id)
```