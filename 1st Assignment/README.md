## Dev Setup

Setup a virtual environment and install the requirements.

```bash
python3 -m venv .venv
. .venv/bin/activate
```

Install dependencies

```bash
pip3 install -r requirements.txt
```

update the firebase config in `app.py` with your own firebase credentials

```python
"apiKey": "",
"authDomain": "",
"projectId": "",
"storageBucket": "",
"messagingSenderId": "",
"appId": "",
```

Run application

```bash
python3 app.py
```
