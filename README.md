# Khmer text summarizer
A simple python project for summarize khmer text.

### Setup python `venv`

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Run summarizer:
```
python khmer-text-summarizer.py -f [file-name] -t [number of summarize sentences]
```

### Example

```
python khmer-text-summarizer.py -f khmer.txt -t 1
```


### Ref
- https://github.com/edubey/text-summarizer