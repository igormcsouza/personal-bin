import argparse
import os
import csv

import openai


class ChatGPT:
    def __init__(self, api_key):
        openai.api_key = api_key

    def ask(self, question: str) -> str:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=question,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.7,
        )

        answer = response.choices[0].text.strip()
        return answer


class RegexChatGPT(ChatGPT):
    @staticmethod
    def _read_csv_file(file_path):
        data = []
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                data.append(row)
        return data

    @staticmethod
    def _is_valid_path(path):
        # Check if the path exists and is a file
        return os.path.exists(path) and os.path.isfile(path)

    def ask(self, question: str) -> str:
        prompts, regexs = [], []

        if self._is_valid_path(question):
            prompts = self._read_csv_file(question)
        else:
            prompts = [question.split(',')]

        for p in prompts:
            regexs.append(super().ask(
                f"Give me a regex that match the following values: {''.join(p)}"))

        return regexs


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ask a question to ChatGPT')
    parser.add_argument('-q', '--question', type=str,
                        required=False, help='The question to ask')
    parser.add_argument('-r', '--regex', type=str, required=False,
                        help='Path or String containing the regex examples')
    args = parser.parse_args()

    api_key = os.environ.get("OPENAI_API_KEY")
    if api_key is None:
        print("Please set your OpenAI API key as an environment "
              "variable: OPENAI_API_KEY")
        exit()

    if args.question:
        chat = ChatGPT(api_key)
        question = args.question
    elif args.regex:
        chat = RegexChatGPT(api_key)
        question = args.regex
    else:
        print("Wrong choice, uses -h for help")
        exit()

    answer = chat.ask(question)

    print(answer)
