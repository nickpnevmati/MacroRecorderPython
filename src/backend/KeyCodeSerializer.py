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
        return []
