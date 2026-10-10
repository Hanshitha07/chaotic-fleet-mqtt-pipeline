from typing import Set

PROCESSED_MESSAGE_IDS: Set[str] = set()

def is_duplicate_message(message_id: str) -> bool:
    """
    Checks if message_id exists in cache.
    If new: registers ID and returns False.
    If already seen: returns True (Duplicate).
    """
    if not message_id:
        return False
        
    if message_id in PROCESSED_MESSAGE_IDS:
        return True
    
    PROCESSED_MESSAGE_IDS.add(message_id)
    return False