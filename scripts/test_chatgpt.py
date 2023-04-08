from unittest.mock import patch, MagicMock

import pytest
from chatgpt import ChatGPT


def assertEqual(response, expected):
    assert response == expected


@patch('openai.Completion.create')
def test_ask(mock_completion_create):
    mock_response = MagicMock()
    mock_response.choices[0].text.strip.return_value = 'The meaning of life is 42.'
    mock_completion_create.return_value = mock_response

    api_key = 'test-api-key'
    chat = ChatGPT(api_key)
    question = 'What is the meaning of life?'
    answer = chat.ask(question)

    mock_completion_create.assert_called_once_with(
        engine="text-davinci-002",
        prompt=question,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )
    assertEqual(answer, 'The meaning of life is 42.')

@pytest.fixture
def mock_gpt_api():
    with mock.patch('openai.api.Completion.create') as mock_create:
        mock_create.return_value.choices[0].text = '.*\\d.*'
        yield

def test_ask_single_question(mock_gpt_api):
    chatbot = RegexChatGPT('YOUR_API_KEY')
    regex = chatbot.ask('What is the meaning of life?')
    assert regex == ['.*\\d.*']

def test_ask_multiple_questions(mock_gpt_api):
    chatbot = RegexChatGPT('YOUR_API_KEY')
    regexes = chatbot.ask('25,26,85,48')
    assert regexes == ['.*\\d.*']

def test_ask_csv_file(mock_gpt_api):
    chatbot = RegexChatGPT('YOUR_API_KEY')
    regexes = chatbot.ask('example.csv')
    assert regexes == ['.*\\d.*', '^[a-zA-Z0-9\\.\\/]*\\.txt$', '^[a-zA-Z0-9\\.\\/]*\\.md$']

