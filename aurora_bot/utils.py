import json

color_emoji_map = {
    "Green": "🟩",  # Green
    "Yellow": "🟨",  # Yellow
    "Orange": "🟧",  # Orange
    "Red": "🟥",  # Red
    "Maroon": "🟫",  # Brown
}

def update_uids(chat_id, file_path):
    """
    Update user IDs.
    
    Args:
        chat_id (str): The chat ID to update.
        file_path (str): The path to the JSON file storing user IDs.
    """
    uids = get_uids(file_path)
    
    if chat_id not in uids:
        uids.append(chat_id)
        
        with open(file_path, 'w') as f:
            json.dump({'uid': uids}, f)


def get_uids(file_path):
    """
    Retrieve user IDs.
    
    Args:
        file_path (str): The path to the JSON file storing user IDs.
    
    Returns:
        list: A list of user IDs.
    """
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data.get('uid', [])
    except FileNotFoundError:
        return []
