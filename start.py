import subprocess as sp
import multiprocessing as mp
import appdirs
import os
import pathlib
import sys
import time

appname = "ScreenParser"
appauthor = "ardasener"
root_dir = appdirs.user_data_dir(appname, appauthor)

requirements = [
    "opencv-python",
    "easyocr",
    "scikit-learn",
    "appdirs",
    "flask",
    "flask-cors"
]

proj_dir = pathlib.Path(__file__).parent.resolve()
backend_dir = os.path.join(proj_dir, "backend")
pip_path = os.path.join(root_dir, "pyenv", "bin", "pip")
python_path = os.path.join(root_dir, "pyenv", "bin", "python")
flask_path = os.path.join(root_dir, "pyenv", "bin", "flask")

def setup_backend(python_exe):
    pathlib.Path(root_dir).mkdir(parents=True, exist_ok=True)
    sp.run([python_exe, "-m", "venv", "pyenv"], cwd=root_dir)
    sp.run([pip_path, "install"] + requirements)

# Will do the following:
# - Create a venv if it does not exist already
# - Install all the dependencies with pip
# - Run the flask backend
def start_backend(python_exe):
    sp.run([flask_path, "run"], cwd=backend_dir)

def start_frontend():
    sp.run(["yarn"], cwd=proj_dir)
    sp.run(["yarn", "electron:serve"])

python_exe = "python"
if len(sys.argv) > 1:
    python_exe = sys.argv[1]

setup_backend(python_exe)

bp = mp.Process(target=start_backend, args=(python_exe,))
bp.start()

time.sleep(2)

fp = mp.Process(target=start_frontend)
fp.start()

bp.join()
fp.join()