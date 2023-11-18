## Install `gptconsole`

```
conda create -n gptconsole_env -c conda-forge python=3.12 -y
conda activate gptconsole_env
python -m pip install gptconsole
```

Make a file in your home directory called `.gptconsolerc`

Add the following contents to the file:

`~/.gptconsolerc`
```
{
    "base_path": "/home/john_vm/conda/envs/gptconsole_env/lib/python3.12/site-packages/",
    "editor_command": "{your editor command}",
    "api_key": "{your api key}",
    "temporary_dir": "/tmp/"
}
```

You can get an API key [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-api-key).
Note that there is a charge for using the API. 
The cost depends on model fidelity.
Pricing is available [here](https://openai.com/pricing).

Use a command-line editor of your choice. I use Emacs. You can use it too, or use `nano`.
E.g.:`"editor_command": "emacsclient --create-frame"` or `"editor_command": "nano"`.

## Use `gptconsole` as a command-line program

In a terminal with the right environment activated, type
```
gpt
```

The prompt changes to 
```
>
```

Enter your prompt and hit enter. You can then enter a follow-up prompt.
You can also enter commands. You can see a list of available commands by typing `\help`.

To access it directly without having to activate the environment, you can create an alias. The way to do this depends on what kind of shell your terminal is running. Aliasing plus using a hotkey to launch a terminal is a very efficient workflow.

## Use `gptconsole` as a python module

See example script.
Note that you can obviously use the `openai` API directly without having to deal with `gptconsole`, which will enable far greater flexibility in what you can achieve programmatically.

### As a literature review aid

Go to compendex and make a search. Narrow down the results as much as possible to manually remove irrelevant results, since each openai API call costs money.

Consider the following search as an example:
```
https://www.engineeringvillage.com/search/quick.url?SEARCHID=8c879b522c9d4843a879d1ca924cc5eb&COUNT=1&usageOrigin=header&usageZone=evlogo
```
Display: 100 results per page, to show all results.
Select all records by clicking on the checkbox at the top.
For searches that have thousands of results, clicking the top checkbox on the last page will include all of them.
Click the download icon and select Location: My PC, Format: Text(ASCII), Output: Detailed record. File name: records, and save.
Replace the path in the example script.
For the above search, I already have the file there.


## Install the package in development mode



You would want to do this to modify the source code and have the change reflected to your scripts and the command line interface, and to be able to contribute changes.

Set up an environment.
```
conda create -n gptconsole_env_dev -c conda-forge python=3.12 -y
conda activate gptconsole_env_dev
```

Go [here](https://github.com/ioannis-vm/gptconsole) and fork the repo to your own GitHub account.
Then clone the repo from a directory of your choice. The files will be downloaded to the directory from where you issue the command.

```
cd {where_you_want_the_repo}
git clone https://github.com/{your_profile}/gptconsole
```

Go in and install the package

```
cd gptconsole
python -m pip install -e .
```
