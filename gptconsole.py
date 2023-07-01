import os
import json
import datetime
import argparse
import sys
import openai


class History:
    def __init__(self, name=None):
        self.contents = []
        self.name = name

    def add_message(self, role, content):
        self.contents.append({'role': role, 'content': content})

    def save(self, file_path):
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.contents, f)

    def load(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            self.contents = json.load(f)

    def remove_most_recent_message(self):
        for _ in range(2):
            self.contents.pop()

    def print_contents(self):
        for item in self.contents:
            if item['role'] == 'user':
                print(f"> {item['content']}")
            else:
                print_response(item['content'])

class OpenAIInterface:
    def __init__(self, model='gpt-3.5-turbo'):
        self.model = model
        self.history = History()
        self.openai_api_key = None

    def set_api_key(self, api_key):
        self.openai_api_key = api_key
        openai.api_key = api_key

    def replace_common_instructions(self, query):
        query = query.replace(
            '#concise', 'Respond clearly and concisely.'
        )
        query = query.replace(
            '#detailed',
            'Provide a very detailed response, but only if you '
            'have high confidence in the accuracy and correctness '
            'of the facts you will outline. Do not include a '
            'conclusion in your response.',
        )
        return query

    def get_response(self, query):
        query = self.replace_common_instructions(query)

        try:
            self.history.add_message('user', query)
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{'role': 'system', 'content': 'You are a helpful assistant.'}]
                + self.history.contents,
                )
            self.history.add_message('assistant', response.choices[0].message.content)
            return response.choices[0].message.content
        except(openai.error.InvalidRequestError) as err:
            print('Oops! There was a problem with the request:')
            print(err)
            print('(Note: History left unchanged.)')
            return None

class CommandLineInterface:

    def __init__(self):
        self.api_interface = OpenAIInterface()
        self.editor_command = None
        self.base_path = None

    def load_config(self):
        home = os.getenv('HOME')
        config_path = os.path.join(home, '.gptconsolerc')
        with open(config_path, 'r') as f:
            config = json.load(f)
        self.base_path = config['base_path']
        self.editor_command = config['editor_command']
        self.temporary_dir = config['temporary_dir']
        self.api_interface.set_api_key(config['api_key'])

    def handle_input(self, prompt):
        user_input = input(prompt)

        if user_input.startswith('\\'):
            command = user_input.lower()

            if command == r'\help':
                self.print_help()

            elif command == r'\save':
                self.save_chat_history()

            elif command == r'\load':
                self.load_chat_history()

            elif command == r'\clear':
                os.system('clear')

            elif command == r'\history':
                self.api_interface.history.print_contents()

            elif command == r'\multiline':
                user_input = self.get_multiline_input()
                print(f"> {user_input}")
                self.process_query(user_input)

            elif command == r'\docstring':
                user_input = self.get_multiline_input()
                print(f"> {user_input}")
                user_input = (
                    "Write a high-quality elaborate docstring "
                    "for the following function/method. "
                    "Only show the text of the docstring, "
                    f"and nothing else:\n```\n{user_input}\n```\n")
                self.process_query(user_input)

            elif command == r'\rm':
                self.api_interface.history.remove_most_recent_message()

            elif command == r'\clear_name':
                self.api_interface.history.name = None

            else:
                print(f'Invalid command: {user_input}')

        else:
            self.process_query(user_input)

    def print_help(self):
        print('Available commands:')
        print('\\load       - Load a saved chat history')
        print('\\save       - Save the chat history')
        print('\\clear      - Clear the console')
        print('\\history    - Print the chat history')
        print('\\multiline  - Enter multiline input')
        print('\\docstring  - Write a docstring')
        print('\\rm         - Remove the most recent prompt & output')
        print('\\clear_name - Clear the chat history name')
        print()
        print('It is possible to pass the first argument like this:')
        print("  $ gpt 'Say hello!'")
        print()
        print('or even pipe output of other commands, like this:')
        print("  $ git diff | gpt 'Write a commit message based on this diff.' ")

    def save_chat_history(self):
        if self.api_interface.history.name is None:
            suggested_name = self.get_appropriate_name()
        else:
            suggested_name = self.api_interface.history.name

        print('Enter the file path to save the chat: ')
        file_name = input(f'Hit Return to accept the default: {suggested_name}\n')

        if file_name == '':
            file_name = suggested_name

        try:
            file_path = os.path.join(self.base_path, 'saved', file_name)

            self.api_interface.history.save(file_path)
            print('Chat saved successfully!')
            self.api_interface.history.name = file_name

        except FileNotFoundError:
            print(f'Error saving file in path: {file_name}\nTry a different path.')
            self.save_chat_history()

    def load_chat_history(self):
        print('Enter the file name to load the chat.')
        list_files_by_last_modified(os.path.join(self.base_path, 'saved'))
        print()
        file_name = input('File (hit Return to abort): ')

        if file_name == '':
            return

        try:
            file_path = os.path.join(self.base_path, 'saved', file_name)
            self.api_interface.history.load(file_path)
            self.api_interface.history.name = file_name
            print('Chat loaded successfully!')

        except FileNotFoundError:
            print(f'File not found: {file_path}. Please check the path and retry.')

    def get_multiline_input(self):
        os.system(f'rm -rf {self.temporary_dir}chatgpttempfile')
        os.system(f'{self.editor_command} {self.temporary_dir}chatgpttempfile')
        with open(f'{self.temporary_dir}chatgpttempfile', 'r', encoding='utf-8') as f:
            user_input = f.read()
        os.system(f'rm -rf {self.temporary_dir}chatgpttempfile')

        return user_input

    def get_appropriate_name(self):
        suggested_name = self.api_interface.get_response(
            'What would be an appropriate concise name '
            'for the previous conversation? '
            'Use as few words as possible.'
        )
        suggested_name = suggested_name.lower().replace(' ', '_').replace('.', '')
        self.api_interface.history.remove_most_recent_message()
        return suggested_name

    def process_query(self, query):
        response = self.api_interface.get_response(query)
        if response:
            print_response(response)

    def run(self, args):

        self.load_config()

        first_prompt = " ".join(args)

        if not sys.stdin.isatty():
            input_stream = sys.stdin.read()
            print(f"'''\n{input_stream}\n'''\n")
        else:
            input_stream = None

        if first_prompt:
            if input_stream:
                response = self.api_interface.get_response(
                    f"'''\n{input_stream}\n'''\n{first_prompt}"
                )
            else:
                response = self.api_interface.get_response(first_prompt)

            if response:
                print_response(response)

        while True:
            try:
                self.handle_input('> ')
            except (KeyboardInterrupt, EOFError):
                break


def list_files_by_last_modified(path):
    files = []

    for item in os.scandir(path):
        if item.is_file():
            last_modified = datetime.datetime.fromtimestamp(item.stat().st_mtime)
            files.append((item.name, last_modified))

    files.sort(key=lambda x: x[1])
    files.reverse()
    print('Last modified                File name')

    for item, last_modified in files:
        print(f'{last_modified}   {item}')

def print_response(text):
    if '\n' in text:
        print('\n\n\n---\n')
        print(text)
        print('\n---\n\n\n')
    else:
        print(text)


if __name__ == '__main__':
    cli = CommandLineInterface()
    cli.run(sys.argv[1:])
