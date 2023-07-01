# gptconsole
Interact with OpenAI's GPT via the command line.

## Installation

- Using a dedicated conda environment is recommended.

```
conda create --name gptconsole-pypi python=3.11 -y
conda activate gptconsole-pypi
python -m pip install gptconsole
```

- Create a `.gptconsolerc` file in your home directory with the following contents:

```
{
    "base_path": "/absolute/path/to/directory/to/store/stuff",
    "editor_command": "youreditor -flags -flags",
    "api_key": "your OpenAI API key",
    "temporary_dir": "/absolute/path/to/a/directory/to/store/temporary/files"
}

```

Example:

```
{
    "base_path": "/home/john_vm/gptconsole/",
    "editor_command": "emacs -q",
    "api_key": "sssh!",
    "temporary_dir": "/tmp/"
}
```
Instructions on how to get an OpenAI API key can be found [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key).

### Install in development mode

```
conda create --name gptconsole-dev python=3.11 -y
conda activate gptconsole-dev
git clone https://github.com/ioannis-vm/gptconsole
cd gptconsole
python -m pip install -e .
```

## Usage

```
gpt "Say Hello, World!"
git diff | gpt "Write me a concise commit message."
gpt <Enter>
> \help
```
