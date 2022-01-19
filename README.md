# ScreenParser

This program allows detecting and grouping GUI objects on a given screenshot.
It can be used either through a command-line interface or an experimental GUI.

## Requirements

> Tests were conducted on Windows 10 and Arch Linux. No tests were conducted for OSX.
> There is no guarantee that the system will work correctly on untested operating systems.

### Python

These steps are required for both the GUI and the command-line interface.

- Python 3 is required. However it should be a version supported by pytorch (3.6, 3.7 or 3.8).
  - All tests were conducted using Python 3.7
- Rest of the requirements can be found in the `backend/requirements.txt` file. Here it is for reference:

```
opencv-python==4.5.4.60
opencv-contrib-python==4.5.4.60
imagehash
easyocr
flask
flask-cors
appdirs
scikit-learn
crc32c
```

> OpenCV version is locked because newer versions tend to cause problems with EasyOCR. 
> See [this issue](https://github.com/JaidedAI/EasyOCR/issues/633) for more info.

- You can install all these dependencies with the command below
```python
pip install -r backend/requirements.txt
```

> The GUI will do this automatically. But there is no disadvantage to doing it manually as well.

### NodeJS

These are only required if you want to use the experimental GUI

- NodeJS (tested with version 16.13.1)
- yarn (tested with version 1.22.15)

If you don't have these installed already we suggest using node version manager:
- [For UNIX/POSIX](https://github.com/nvm-sh/nvm)
- [For Windows](https://github.com/coreybutler/nvm-windows)

## Running (CLI)

Once the python dependencies are installed you can simply run the `cli.py` file
as shown in the example below.

```bash
cd backend
python cli.py <config_file>
```

The `config_file` used must be in json format. You can obtain this in two ways:
- Simply copy the `default_config.json` file (in the same directory as `cli.py`).
- The GUI will create a config file in the output directory after each run featuring the options used for that run.

The images to be processed can be specified in the config file's "images" option.
This must be a list of absolute paths of the files. See the example below.

```json
{
  "images": ["/home/arda/Projects/screenparserdata/DSLR/MagicLantern2.png", "/home/arda/Projects/screenparserdata/DSLR/MagicLantern1.png"],
  ...
}
```

> On Windows, the default "\" separators can cause problems with json (you will probably see an encoding related error.
> In these cases use paths with UNIX style "/" separators or with escaped separators "\\".

## Running (GUI)

Once the python and nodejs dependencies are installed. 
You can start the GUI by doing the following:

```bash
yarn
yarn electron:serve
```

> First command will install the dependencies, the second command will start the program.

> It is technically possible to build the application and distribute it in binary form.
> However I wasn't able to iron out the bugs in the release version (mostly related to file paths).

## Using the GUI

At the start the GUI will ask you to enter the python executable. 
You need to ensure this is a python of version 3.6, 3.7 or 3.8.
If this is all you have installed on your system then you can probably leave it default.
Otherwise you should provide the path to the desired version of python.

> Alternatively one can create a virtual environment and pass the python in the bin directory of that environment.
> See [this](https://docs.python.org/3/library/venv.html) for more info about virtual environments.

Once the user enters the executable and presses the button. 
The GUI will automatically install the python dependencies using `pip`
and then run the backend application which it will start communicating with.

The user can then select the image files they want to be processed
and click the green button in the bottom right corner of the screen.
The first run may take longer since the OCR process takes a decent amount of time.
However after the first run the OCR data will be cached and reused in later runs
unless the OCR related options are changed. These cache files are stored in a temporary 
directory as a result they will likely be deleted once the operating system shuts down.

After the first run, the user can move between different steps of the algorithm
using the menu at the very top. Options can be changed from the GUI and clicking the
green button again will rerun the algorithm with the changed options and automatically
update the results shown in the GUI. 
The images shown in these screens can be clicked on to take a closer look.

As mentioned previously, the GUI will also produce a config file in the output directory
alongside the regular xml output. This config file can be used in the command-line interface.
The ideal use case here is for the user to use the GUI to fine tune the algorithm and then
use the exported config file to automate the process.

## Known Bugs

### Broken Pipe

Occasionally the GUI might give a broken pipe error.
If this occurs the green run button will turn red and clicking on it will print the error.
I was not able to detect the cause of this problem.
However, usually just clicking run again fixes the issue temporarily.

### Backend Termination

Backend might not always terminate after the GUI app is closed.
It will not use too many resources however and can be manually killed from a system monitor.

### Filenames

Filenames containing keywords like detection, clustering etc. might be displayed wrongly on the GUI.
There is an easy fix for this but it was not implemented due to time constraints.