<img src="https://i.imgur.com/uuWWP39.png" alt="jarvis banner" />

# jarvis

Jarvis is a simple IA for home automation / personal assistant with voice commands written in Python. It can be used
alongside with HomeAssistant, the more devices you have on HomeAssistant, the more you will be able to teach to Jarvis.

**This is only the server-side of Jarvis, you can download the client [here](https://github.com/M4TH1EU/jarvis-client)
.**

### Languages

It only supports French and English (normally) for now, but with some changes you should be able to use english or
another language.

### Compatibility

The server can run on anything that runs Python 3+ *(linux recommended)*

## Installation

If not already installed, you will need Python 3.9 and few other packages for jarvis to work, you can install them with
these commands.

```shell
$ sudo add-apt-repository ppa:deadsnakes/ppa
$ sudo apt-get update
$ sudo apt install python3.9 python3.9-dev python3.9-distutils python3-fann2 libfann-dev swig
```

After that, run the command `python -m pip3 install -r requirements.txt` to install the basic requirements for the
project.

Then we need to train our model, but before that we need to download "punkt" and "stopwords" from the NLTK downloader,
go to the Python Console and enter the following commands :

```shell
> import nltk
> nltk.download('punkt')
> nltk.download('stopwords')
```