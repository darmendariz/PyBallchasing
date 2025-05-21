import os
from dotenv import load_dotenv
import requests 

class BallchasingAPI:
    """
    A class that acts as a Python wrapper to call the Ballchasing API. 
    See https://ballchasing.com/api/docs.
    """

    def __init__(self, api_key:str=None):
        self.api_key = api_key if api_key is not None else self.get_api_key()
        self.base_url = "https://ballchasing.com/api"
        self.headers = {"Authorization" : self.api_key}

    def get_api_key(self):
        """
        Fetches your Ballchasing API key. Assumes the key is stored in a .env file in the current directory in the form BALLCHASING_API_KEY="__________" .
        """
        load_dotenv()
        api_key = os.environ.get("BALLCHASING_API_KEY")
        if api_key:
            return api_key
        else:
            print("API key not found. Please set the BALLCHASING_API_KEY in your .env file.")
            return -1

    # PING -----------------------------------------------------------------------------------
    def ping(self):
        """
        Pings the Ballchasing API to check if it's reachable and verifies that the API key is valid.
        See https://ballchasing.com/doc/api#ping.
        """
        r = requests.get(self.base_url, headers=self.headers)
        if r.status_code == 200:
            print("API is reachable and API key is valid.")
            return True
        elif r.status_code == 401:
            print(f"Invalid API key. Status code: {r.status_code}.")
            return False
        elif r.status_code == 500:
            print(f"Ballchasing API is not reachable. Status code: {r.status_code}.\n")
            print(r.text)
            return False
        
    # UPLOAD -----------------------------------------------------------------------------------
    # TODOS:
    #   - fix/check upload filename; add default behavior or allow user to supply custom name  
    #   - deal with group id parameter functionality 
    #   - test 
    def upload_replay(self, path_to_replay:str, params:dict={"visibility":"public"}):
        """
        Uploads a replay file to ballchasing.com. Can optionally supply the visibility and group id for the uploaded replay as params.
        See https://ballchasing.com/doc/api#upload-upload-post.
        """
        if 'visibility' not in params:
            params['visibility'] = 'public'

        url = f"{self.base_url}/v2/upload?visibility={params['visibility']}"
        files = {"file": open(path_to_replay, "rb")}

        r = requests.post(url, headers=self.headers, files=files)

        if r.status_code == 201:
            print("Replay uploaded successfully.")
            return r.json()['id']
        elif r.status_code == 409:
            print(f"Error: duplicate replay with id {r.json()['id']} and location {r.json()['location']}. Status code: {r.status_code}.")
            return r.json()['id']
        elif r.status_code == 400:
            print(f"Error: {r.json()['error']}. Status code: {r.status_code}.")
            return r.json()['error']
        elif r.status_code == 500:
            print(f"Error: {r.json()['error']}. Status code: {r.status_code}.")
            return r.json()['error']

    # REPLAYS ----------------------------------------------------------------------------------
    def list_filter_replays(self, params:dict=None):
        """
        Lists replays using the provided dictionary of filter parameters.
        See https://ballchasing.com/doc/api#replays-replays-get for valid parameters. 
        """
        url = f"{self.base_url}/replays"
        r = requests.get(url, headers=self.headers, params=params)
        if r.status_code == 200:
            return r.json()
        else:
            print(f"Failed to list replays. Status code: {r.status_code}.")
            return None
        
    def get_replay_info(self, replay_id:str):
        """
        Fetches replay details and info using the replay ID.
        See https://ballchasing.com/doc/api#replays-replay-get.
        """
        url = f"{self.base_url}/replays/{replay_id}"
        r = requests.get(url, headers=self.headers)
        if r.status_code == 200:
            return r.json()
        else:
            print(f"Failed to fetch replay {replay_id}. Status code: {r.status_code}.")
            return None
        
    # TODOS
    #   - test
    def delete_replay(self, replay_id:str):
        """
        WARNING: This operation is permanent and cannot be undone.
        
        Deletes a replay from ballchasing.com using the replay ID.
        See https://ballchasing.com/doc/api#replays-replay-delete.
        """
        url = f"{self.base_url}/replays/{replay_id}"
        r = requests.delete(url, headers=self.headers)
        if r.status_code == 204:
            print(f"Replay {replay_id} deleted successfully.")
            return True
        return False

    # TODOS
    #   - test
    def patch_replay(self, replay_id:str, params:dict):
        """
        WARNING: This operation is permanent and cannot be undone.

        Patches one or more fields of the replay using the replay ID and a dictionary of fields to be patched.
        See https://ballchasing.com/doc/api#replays-replay-patch.
        """
        url = f"{self.base_url}/replays/{replay_id}"
        r = requests.patch(url, headers=self.headers, json=params)
        if r.status_code == 204:
            print(f"Replay {replay_id} patched successfully.")
            return True
        return False 

    # TODOS
    #   - test
    def download_replay_file(self, replay_id:str):   
        """
        Downloads a replay file using the replay ID.
        See https://ballchasing.com/doc/api#replays-replay-get-1. 
        """
        url = f"{self.base_url}/replays/{replay_id}/file"
        r = requests.get(url, headers=self.headers)
        if r.status_code == 200:
            with open(f"{replay_id}.replay", "wb") as f:
                f.write(r.content)
            print(f"Replay {replay_id} downloaded successfully.")
        else:
            print(f"Failed to download replay {replay_id}. Status code: {r.status_code}.")

    # REPLAY GROUPS -----------------------------------------------------------------------------
    # TODOS
    #   - test
    def create_group(self, group_name:str, player_identification:str, team_identification:str, parent_id:str=None):
        """
        Creates a new replay group using the group name, player identification, and team identification. Optionally, can supply a parent group id to create the new group as a child of the specified parent group. 
        See https://ballchasing.com/doc/api#replay-groups-groups-post. 
        """
        url = f"{self.base_url}/groups"
        data = {
            "name": group_name,
            "player": player_identification,        # Choices: 'by-id' or 'by-name'
            "team": team_identification             # Choices: 'by-distinct-players' or 'by-player-clusters'
        }
        if parent_id is not None:
            data["parent"] = parent_id

        r = requests.post(url, headers=self.headers, json=data)
        if r.status_code == 201:
            print(f"Group '{group_name}' created successfully.")
            return r.json()
        else:
            print(f"Failed to create group '{group_name}'. Status code: {r.status_code}.")
            return None

    def list_filter_groups(self, params:dict=None):
        """
        Lists replay groups and child groups using the provided dictionary of filter parameters.
        See https://ballchasing.com/doc/api#replay-groups-groups-get for valid parameters. 
        """
        url = f"{self.base_url}/groups"
        r = requests.get(url, headers=self.headers, params=params)
        if r.status_code == 200:
            return r.json()
        else:
            print(f"Failed to filter groups. Status code: {r.status_code}.")
            return None

    def get_group_info(self, group_id:str):
        """
        Fetches group info and stats using the group ID.
        See https://ballchasing.com/doc/api#replay-groups-group-get.
        """
        url = f"{self.base_url}/groups/{group_id}"
        r = requests.get(url, headers=self.headers)
        if r.status_code == 200:
            return r.json()
        else:
            print(f"Failed to fetch group {group_id}. Status code: {r.status_code}.")
            return None

    # TODOS
    #   - test
    def delete_group(self, group_id:str):
        """
        WARNING: This operation is permanent and cannot be undone.

        Deletes the specified group using the group id. 
        See https://ballchasing.com/doc/api#replay-groups-group-delete.
        """
        url = f"{self.base_url}/groups/{group_id}"
        r = requests.delete(url, headers=self.headers)
        if r.status_code == 204:
            print(f"Group {group_id} deleted successfully.")
            return True
        else:
            print(f"Failed to delete group {group_id}. Status code: {r.status_code}.")
            return False
        return 
    
    # TODOS
    #   - test
    def patch_group(self, group_id:str, params:dict):
        """
        WARNING: This operation is permanent and cannot be undone.

        Patches one or more fields of the group using the group ID and a dictionary of fields to be patched.
        See https://ballchasing.com/doc/api#replay-groups-group-patch.
        """
        url = f"{self.base_url}/groups/{group_id}"
        r = requests.patch(url, headers=self.headers, json=params)
        if r.status_code == 204:
            print(f"Group {group_id} patched successfully.")
            return True
        else:
            print(f"Failed to patch group {group_id}. Status code: {r.status_code}.")
            return False

    # MISC --------------------------------------------------------------------------------------
    # TODOS
    #   - test
    def get_maps(self):
        """
        Gets a dictionary that connects map codes to in-game map names.
        See https://ballchasing.com/doc/api#misc-maps-get.
        """
        url = f"{self.base_url}/maps"
        r = requests.get(url, headers=self.headers)
        if r.status_code == 200:
            return r.json()
        else:
            print(f"Failed to fetch maps. Status code: {r.status_code}.")
            return None
