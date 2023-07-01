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

## Usage

```

gptconsole "Say Hello, World!"
git diff | "Write me a concise commit message."
gptconsole
> \help

```
