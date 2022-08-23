def add_spaces(text: str) -> str:
    """Converts camel case to regular case with spaces.

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

        result += char

    return result.capitalize()
