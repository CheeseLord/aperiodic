May need to install pyqt to system Python before it will work in a virtualenv,
something like:

```
sudo apt install pyqt5-dev-tools
```

Create a virtualenv and install requirements.txt:

```
python3 -m venv VENV_DIR
VENV_DIR/bin/pip install -r requirements.txt
```
