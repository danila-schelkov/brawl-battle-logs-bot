TAG_CHARS = '0289PYLQGRJCUV'


def clean_tag(tag: str) -> str:
    """Clean the tag

    :param tag: account tag
    :type tag: str
    :rtype: str
    :return: tag without # and with 0, 8 instead O and B
    """

    return tag.upper().replace('#', '').replace('O', '0').replace('B', '8')


def add_spaces(text: str) -> str:
    """Clean the tag

    :param text: camelCase text
    :type text: str
    :rtype: str
    :return: text with spaces like "Camel case"
    """

    result = ''
    for char_index in range(len(text)):
        char = text[char_index]

        if char.isupper():
            result += ' '
        if char_index == 0:
            char = char.upper()

        result += char

    return result
