# Z-Game Team Chris 1

BWSI-SG with AI Zombie Game.

## Prerequisites

First, you need to have Python on your system. Open either `cmd` (Windows) or Terminal (macOS) and type `python --version`. 
If this throws an error, or shows a version less than Python 3.7, 
you'll need to install it from [here](https://www.python.org/downloads/release/python-376/).
 Once your install has finished, running `python --version` should show `3.7.6`.

Then, install Anaconda using one of the graphical 
installers [found here](https://www.anaconda.com/products/individual). 
You want to get the installer that runs under Python 3.7. 
This will contain the `conda` command line tool and the Anaconda Navigator. 
This will be where you go to start up Jupyter Notebook. 
Once installed, you can use `conda --version` to verify installation.

Also, ensure Git is setup properly. For a Git primer, check out this [help page](https://docs.github.com/en/github/getting-started-with-github/set-up-git)

## Getting Started
Quick start from a command prompt:
```
git clone git@github.mit.edu:BWSI-SGAI-2020/ZGame.git
cd ZGame
conda env create -f zgame_env.yml
conda activate zgame
```

This will get all the repository files on your system and then use conda to create and 
activate the environment. This will contain all required dependencies. 
Python files in the main directory can be run to get an idea of how to use the game.

# Game Details
Out of the box, this is a command line interface (CLI) game and can be ran from a command prompt (or terminal) or 
from an integrated development environment (IDE). The entry points for the code have "RUN" as a prefix.

For example, to run basic tests, use the following command. NOTE: this command prints the help commands
for the CLI options. It will show you the usage and options for the CLI.
```
python RUN_Basic.Tests.py -h
```

More details about the game and this software implementation will be provided over time via lectures.
