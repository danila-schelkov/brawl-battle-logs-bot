from utilities import id_to_tag, tag_to_id


class Profile:
    class Id:
        high: int
        low: int

        def from_tag(self, tag: str):
            self.high, self.low = tag_to_id(tag)

        def from_long_id(self, value: int):
            self.high = value % 256
            self.low = (value - self.high) >> 8

        def to_tag(self) -> str:
            return id_to_tag(self.high, self.low)

    def __init__(self):
        self._id: Profile.Id = Profile.Id()
        self.last_battle_timestamp: int = -1

    def load(self, data):
        self._id.from_long_id(data[0])
        self.last_battle_timestamp = data[1]

    def get_tag(self) -> str:
        return self._id.to_tag()

    def get_id(self) -> int:
        return (self._id.low << 8) + self._id.high
