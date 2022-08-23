TAG_CHARS = '0289PYLQGRJCUV'


def _clean_tag(tag: str) -> str:
    """Clean the tag.

    :param tag: account tag
    :type tag: str
    :rtype: str
    :return: tag contains only chars 0289PYLQGRJCUV
    """

    return tag.strip().upper().replace('#', '').replace('O', '0').replace('B', '8')


def tag_to_id(tag: str) -> tuple[int, int]:
    """Converts tag to a pair of high and low ids.

    :param tag: account tag
    :return: high and low ids
    """
    tag = _clean_tag(tag)
    value = 0

    for char in tag:
        value *= len(TAG_CHARS)
        value += TAG_CHARS.index(char)

    high = value % 256
    low = (value - high) >> 8

    return high, low


def id_to_tag(high_id: int, low_id: int) -> str:
    """Converts a pair of high and low ids to tag.

    :param high_id:
    :param low_id:
    :rtype: str
    :return: account tag
    """

    id_value = (low_id << 8) + high_id
    tag = []

    while id_value > 0:
        tag.insert(0, TAG_CHARS[int(id_value % len(TAG_CHARS))])
        id_value -= id_value % len(TAG_CHARS)
        id_value /= len(TAG_CHARS)

    return ''.join(tag)
