# About 

PyBallchasing is a wrapper for the [ballchasing API](https://ballchasing.com/doc/api) that allows users to call the API in pure Python.  

[Ballchasing](https://ballchasing.com) is a repository consisting of more than 130,000,000 Rocket League replay files that provide a replay of matches played in-game in a proprietary binary file format. With the API, users can 
- download, upload, delete, and patch replays, 
- create replay groups to organize collections of replays in a tree-like structure, and 
- access basic information and statistics about replays or replay groups. 

# Example usage

## Authentication 

All calls to the Ballchasing API must be authenticated with an [API key](https://ballchasing.com/doc/api#header-authentication). By default, the `BallchasingAPI` class will search for a `.env` file in the current directory and extract the key from it. You can store your key by writing the following line in your `.env` file:

> BALLCHASING_API_KEY = "my_api_key"

An instance of the `BallchasingAPI` class can then be created like so: 
```python
bc = BallchasingAPI()
```
Alternatively, you can pass the key directly into the initializer:
```python
bc = BallchasingAPI("my_api_key")
```

The API key is stored as an instance variable `self.api_key` with each class instance; once initialized, users can make multiple calls without manually re-authenticating, e.g.: 
```
>>> bc.get_replay_info(replay_id)
>>> bc.download_replay(replay_id)
```

## Checking the connection

You can verify your key and check for a valid connection to the API by calling the `ping()` method:
``` 
>>> bc = BallchasingAPI()
>>> bc.ping()
API is reachable and API key is valid.
True
```

# Installation
