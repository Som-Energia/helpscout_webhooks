# Installation & Usage

## Install pipenv
```bash
sudo -H pip install pipenv
```

## Install project dependencies
```bash
pipenv install
```

## Run server
```bash
pipenv run python run.py
```

## Run tests
```bash
pipenv run python -m unittest discover -p *_test.py
```

# Changelog

## v2.0.0
- Use [v2 helpscout Payload](https://developer.helpscout.com/mailbox-api/endpoints/conversations/get/#response)

## v1.0.0
- First webhook version. Require [v1 helpscout Payload](https://developer.helpscout.com/webhooks/objects/conversation/)