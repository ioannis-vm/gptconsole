# gpt_term
Interact with OpenAI's GPT via the command line.

## Installation instructions

- Instantiate an environment and install dependencies.

```
conda create --name opnai python=3.11 -y
python -m pip install openai
```

- Create an API key and store it as `api_key` right next to `chat_gpt.py`.

- Modify the `BASE_PATH` variable in `chat_gpt.py` to point to the directory where it is stored.

- Create a `saved` directory in which saved chats will be placed.

- Provide an alias to the python script execution, for convenience. For example:

```
echo 'alias gpt="/home/john_vm/miniconda3/envs/opnai/bin/python /home/john_vm/openai/chatgpt.py"'
```
