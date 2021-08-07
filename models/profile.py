from utilities import TAG_CHARS, clean_tag


class Profile:
    class Id:
        high: int
        low: int

    _id: Id
    last_battle_timestamp: int

    def load(self, data):
        self.id = data[0]
        self.last_battle_timestamp = data[1]

    def get_tag(self) -> str:
        _id = (self._id.low << 8) + self._id.high
        tag = []

        while _id > 0:
            tag.insert(0, TAG_CHARS[int(_id % len(TAG_CHARS))])
            _id -= _id % len(TAG_CHARS)
            _id /= len(TAG_CHARS)

        return ''.join(tag)

    def set_tag(self, tag: str):
        tag = clean_tag(tag)
        _id = 0

        for char in tag:
            _id *= len(TAG_CHARS)
            _id += TAG_CHARS.index(char)

        self.id = _id

    def get_id(self) -> int:
        return (self._id.low << 8) + self._id.high

    def set_id(self, value: int):
        self._id = Profile.Id()

        self._id.high = value % 256
        self._id.low = (value - self._id.high) >> 8

    id = property(get_id, set_id)
    tag = property(get_tag, set_tag)
