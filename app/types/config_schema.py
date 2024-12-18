from typing import TypedDict

class ConfigSchema(TypedDict):
    """
    ConfigSchema defines the structure of configuration data 
    required for processing state graph nodes.

    Attributes:
        thread_id (str): Unique identifier for the thread context.
    """
    thread_id: str