import json.decoder

from pynput.keyboard import Key, KeyCode
from src.logger import logger


# Function to serialize Key and KeyCode
def serialize_keys(keys):
    serialized = []
    for key in keys:
        if isinstance(key, Key):
            serialized.append({'type': 'Key', 'value': str(key)})
        elif isinstance(key, KeyCode):
            serialized.append({'type': 'KeyCode', 'value': key.char})
    return json.dumps(serialized)

# Function to deserialize Key and KeyCode
def deserialize_keys(serialized_keys):
    try:
        serialized_keys = json.loads(serialized_keys)
        deserialized = []
        for key_data in serialized_keys:
            if key_data['type'] == 'Key':
                deserialized.append(getattr(Key, key_data['value'].split('.')[1]))
            elif key_data['type'] == 'KeyCode':
                deserialized.append(KeyCode(char=key_data['value']))
        return deserialized
    except json.decoder.JSONDecodeError:
        logger.error(f"Failed to deserialize Hotkey {serialized_keys}")
        return None

# # Example usage
# hotkeys = [Key.alt, KeyCode.from_char('a')]  # A sample list of hotkeys
#
# # Serialize the keys to a file
# with open('keys.json', 'w') as f:
#     json.dump(serialize_keys(hotkeys), f)
#
# # Load and deserialize the keys from the file
# with open('keys.json', 'r') as f:
#     loaded_keys = deserialize_keys(json.load(f))
#
# # Verify the deserialized keys
# print(loaded_keys)  # Output should show the equivalent Key and KeyCode objects
