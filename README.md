# About 

## ballchasing.com
[Ballchasing](https://ballchasing.com) is a repository of over 130 million [Rocket League](https://www.rocketleague.com/en) replay files that record more than 650 million minutes of gameplay time. These files allow players to save and re-watch full replays of matches played in-game using the game client. With the [ballchasing API](https://ballchasing.com/doc/api), users can 
- download, upload, delete, and patch replays, 
- create replay groups to organize collections of replays in a tree-like structure, and 
- access basic information and statistics about replays or replay groups. 

Rocket League replays are encoded in a proprietary and somewhat opaque binary file format `.replay`, but there exist parsing libraries with which users can extract meaningful data from the files (see [boxcars](https://github.com/nickbabcock/boxcars), [rattletrap](https://github.com/tfausak/rattletrap), [subtr-actor](https://github.com/rlrml/subtr-actor), and more). 

## PyBallchasing
PyBallchasing is a wrapper for the [ballchasing API](https://ballchasing.com/doc/api) that allows users to call the API in pure Python.  

# Example usage

## Authentication 

All calls to the Ballchasing API must be authenticated with an [API key](https://ballchasing.com/doc/api#header-authentication). By default, the `BallchasingAPI` class will search for a `.env` file in the current directory and extract the key from it at initialization. You can store your key by writing the following line in your `.env` file:

> BALLCHASING_API_KEY = "my_api_key"

An instance of the `BallchasingAPI` class can then be created like so: 
```python
bc = BallchasingAPI()
```
Alternatively, you can pass the key directly into the initializer:
```python
bc = BallchasingAPI("my_api_key")
```

The API key is stored as an instance variable `self.api_key`. After a class instance is initialized with a valid key, users can make multiple calls to the API without manually re-authenticating, e.g.: 
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

## Calling the API 
### Getting replay information
To get stats/info on a specific replay, call `get_replay_info()`:
```python
bc = BallchasingAPI()
replay_id = "8fbf7071-e77d-4f2b-9963-fb12e18dda4b"
info = bc.get_replay_info(replay_id)
print(info)
```
This produces the following output (pretty-printed for readability):
```
{'blue': 
    {'color': 'blue',
    'name': 'TEAM BDS',
    'players': [{'camera': {'distance': 240,
                            'fov': 110,
                            'height': 100,
                            'pitch': -3,
                            'stiffness': 0.7,
                            'swivel_speed': 4.2,
                            'transition_speed': 1.4},
                'car_id': 4284,
                'car_name': 'Fennec',
                'end_time': 351.99057,
                'id': {'id': '76561199013057612',
                'platform': 'steam'},
                'mvp': True,
                'name': 'Seikoo',
                'start_time': 0,
                'stats': {'boost': {'amount_collected': 2126,
                                    'amount_collected_big': 1465,
                                    'amount_collected_small': 661,


                    ...and so on...
```
This replay info is for Game 1 of Team BDS vs. G2 Esports in the 2021-2022 RLCS World Championship grand finals. See [here](https://ballchasing.com/replay/8fbf7071-e77d-4f2b-9963-fb12e18dda4b?g=bds-vs-g2-0z2kj5fp08). 
# Installation
