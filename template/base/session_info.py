from enum import Enum
from dataclasses import dataclass

class ClientSessionState(str, Enum):
    NONE = "None"
    FATAL = "Fatal"
    EXPIRED = "Expired"
    DUPLICATED = "Duplicated"
    BLOCKED = "Blocked"
    NETERROR = "NetError"

@dataclass
class SessionInfo:
    user_id: str = ""
    platform_id: str = ""
    platform_type: int = -1
    account_id: str = ""
    account_level: int = 0
    app_version: str = ""
    os: str = ""
    country: str = ""
    session_state: ClientSessionState = ClientSessionState.NONE 