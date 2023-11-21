import uuid
from typing import Optional

from chan.chan import Chan


class ChanManager:
    def __init__(self):
        self.dict: dict[str, Chan] = {}

    def register(self, chan: Chan):
        id = str(uuid.uuid4().hex[:6])
        self.dict[id] = chan

        return id

    def get(self, id) -> Optional[Chan]:
        try:
            return self.dict[id]
        except:
            return None
