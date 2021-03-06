<img src="https://i.imgur.com/uuWWP39.png" alt="jarvis banner" />

# jarvis-server

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

# Errors
Common errors than I personally encoured during this project, hope this can help you.

### FANN/FANN2 error during pip requirements

#### Linux :

First be sure to have all those packages installed : 
```
sudo apt-get install libfann-dev swig libfann-dev python3-fann2
```
I actually don't know how I solved this but I tried building myself FANN following the instruction
from [here](https://github.com/libfann/fann#from-source). Here is some links I found trying to solve the error :
https://stackoverflow.com/questions/51367972/lib-fann2-failed-to-install
https://github.com/FutureLinkCorporation/fann2/issues/11
https://github.com/MycroftAI/padatious#installing
https://github.com/MycroftAI/padatious/issues/21
https://jansipke.nl/installing-fann-with-python-bindings-on-ubuntu/

#### Windows

Solution for windows users :

```
pip install pipwin
pipwin install fann2
```

### Error 404 from the HomeAssistant API

*/!\ Only Windows usually*  
Returns an error 404 when requesting information about an entity_id, you need to edit the source code of the file "
rawapi.py" from the api.  
Line 53 of rawapi.py must be changed from ``self.endpoint(path),`` to ``self.endpoint(path.replace('\\', '/')),``
