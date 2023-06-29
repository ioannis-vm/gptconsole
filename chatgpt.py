"""
Interact with the openai API via the command line.
"""

# TODO
# Github repo (private)
# Figure out how to deal with pipes.


import os
import json
import argparse
import openai
import datetime
import sys


BASE_PATH = '/home/john_vm/openai/'

if not sys.stdin.isatty():
    input_stream = sys.stdin.read()
    print(f"'''\n{input_stream}\n'''\n")
else:
    input_stream = None

class Interface:

    def __init__(self):
        self.model = "gpt-3.5-turbo"
        self.history = []
        self.name = None

    def get_response(self, query):

        # replace common instructions
        query = query.replace(
            '#concise',
            'Respond clearly and concisely.')
        query = query.replace(
            '#detailed',
            'Provide a very detailed response, but only if you have '
            'high confidence in the accuracy and correctness of the '
            'facts you will outline. Do not include a conclusion in '
            'your response.')

        self.history.append({"role": "user", "content": query})

        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system",
                 "content": "You are a helpful assistant."}]
            + self.history,
        )

        self.history.append(
            {"role": "assistant",
             "content": response.choices[0].message.content}
        )

        return response.choices[0].message.content

    def get_appropriate_name(self):
        suggested_name = self.get_response(
            'What would be an appropriate concise name for the previous conversation? '
            'Important: Only show the name, and NOTHING ELSE.')
        suggested_name = suggested_name.lower().replace(' ', '_').replace('.', '')
        self.forget_once()
        return suggested_name
        

    def save_chat_history(self):

        if self.name is None:
            suggested_name = self.get_appropriate_name()
        else:
            suggested_name = self.name

        print("Enter the file path to save the chat: ")
        file_name = input(f'Hit Return to accept the default: {suggested_name}')
        if file_name == '':
            file_name = suggested_name
        try:
            with open(BASE_PATH + f'saved/{file_name}',
                      'w', encoding='utf-8') as f:
                json.dump(self.history, f)
            print("Chat saved successfully!")
        except FileNotFoundError:
            print(f'Error saving file in path: {file_name}'
                  '\n'
                  'Try a different path.')
            self.save_chat_history()

    def load_chat_history(self):

        print("Enter the file path to load the chat.")
        list_files_by_last_modified(BASE_PATH + 'saved')
        print()
        file_path = input('File (hit Return to abort): ')
        if file_path == '':
            return
        try:
            with open(BASE_PATH + f'saved/{file_path}', 'r', encoding='utf-8') as f:
                self.history = json.load(f)
        except FileNotFoundError:
            print(f'File not found: {file_path}. Please check the path and retry.')
        else:
            print("Chat loaded successfully!")
            self.name = file_path

    def print_history(self):

        for item in self.history:

            if item['role'] == 'user':
                print(f"> {item['content']}")
            else:
                print_response(item['content'])

    def forget_once(self):

        for i in range(2):
            self.history.pop()


def print_response(text):
    if '\n' in text:
        print()
        print()
        print()
        print('---')
        print(text)
        print('---')
        print()
        print()
        print()
    else:
        print(text)


def list_files_by_last_modified(path):

    files = []

    # Iterate over each file in the directory
    for item in os.scandir(path):
        # Check if it is a regular file
        if item.is_file():
            # Get the last modification time
            last_modified = datetime.datetime.fromtimestamp(
                item.stat().st_mtime)
            # Append the file and its last modified time to the list
            files.append((item.name, last_modified))

    # Sort the files list by the last modified time
    files.sort(key=lambda x: x[1])
    files.reverse()

    # Print the list of files and last modified times
    print('Last modified                File name')
    for item, last_modified in files:
        print(f"{last_modified}   {item}")


def handle_input(prompt):

    user_input = input(prompt)

    if user_input.startswith('\\'):

        if user_input.lower() == r"\save":

            gpt.save_chat_history()
            return

        if user_input.lower() == r"\load":

            gpt.load_chat_history()
            return

        if user_input.lower() == r'\clear':
            os.system('clear')
            return

        if user_input.lower() == r'\history':
            gpt.print_history()
            return

        if user_input.lower() == r'\multiline':

            os.system('rm -rf /tmp/chatgpttempfile')
            os.system('emacs -q /tmp/chatgpttempfile')
            with open('/tmp/chatgpttempfile', 'r', encoding='utf-8') as f:
                user_input = f.read()
            print('> ' + user_input)
            return

        if user_input.lower() == r'\docstring':

            os.system('rm -rf /tmp/chatgpttempfile')
            os.system('emacs -q -nw /tmp/chatgpttempfile')
            with open('/tmp/chatgpttempfile', 'r', encoding='utf-8') as f:
                user_input = f.read()
            user_input = (
                'Write a high-quality elaborate docstring '
                'for the following function/method. '
                'Only show the text of the docstring, and nothing '
                f'else:\n```\n{user_input}\n```\n')
            print('> ' + user_input)
            return

        if user_input.lower() == r'\rm':
            gpt.forget_once()
            return

        if user_input.lower() == r'\clear_name':
            gpt.name = None
            return

        print(f'Invalid command: {user_input}')

    else:

        print_response(gpt.get_response(user_input))


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "prompt", nargs='?', type=str,
        default=None, help="First prompt")

    args = parser.parse_args()
    first_prompt = args.prompt

    with open(BASE_PATH+'api_key', 'r', encoding='utf-8') as file:
        api_key = file.read().strip()

    # openai.api_key = os.getenv("OPENAI_API_KEY")
    openai.api_key = api_key

    gpt = Interface()

    if first_prompt:

        if input_stream:
            print_response(
                gpt.get_response(
                    f"'''\n{input_stream}\n'''\n{first_prompt}"))

        else:

            print_response(gpt.get_response(first_prompt))

    # Main loop
    while True:

        try:
            handle_input("> ")

        except (KeyboardInterrupt, EOFError):
            break
