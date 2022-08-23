import abc
import atexit
import configparser
import typing

CONFIG_FILENAME = './config.ini'


class Config:
    def __init__(self):
        self._parser = configparser.ConfigParser()
        self.filename: str or None = None

    def load(self):
        """Loads properties from .ini file to class fields

        :return:
        """

        try:
            self._parser.read(self.filename)
            self._sync_fields()
        except configparser.NoOptionError:
            self.save()

    def save(self):
        """Saves class fields to .ini file

        :return:
        """

        self._sync_properties()
        self._parser.write(open(self.filename, 'w'))

    @abc.abstractmethod
    def _sync_fields(self) -> None:
        """Assigns properties to fields

        :return:
        """

    @abc.abstractmethod
    def _sync_properties(self) -> None:
        """Dumps fields to properties

        :return:
        """

    def get_property(self,
                     section: str,
                     option: str,
                     default_value: typing.Any = None,
                     cast_type: typing.Type = None) -> typing.Any:
        """Returns property from config

        :param section: name of config section (e.g. DEFAULT)
        :param option: name of option in the section
        :param default_value: value that is set if property is empty (by default is None)
        :param cast_type: class for casting the value (e.g. int(value) if int)
        :return:
        """

        value = self._parser.get(section, option)
        if value is None or value == '':
            return default_value

        if cast_type is not None:
            return cast_type(value)

        return value

    def set_property(self, section: str, option: str, value: typing.Any) -> None:
        """

        :param section: name of config section (e.g. DEFAULT)
        :param option: name of option in the section
        :param value: value to set in the property
        :return:
        """

        if not self._parser.has_section(section) and section != 'DEFAULT':
            self._parser.add_section(section)

        if value is None:
            value = ''

        self._parser.set(section, option, str(value))


class BotConfig(Config):
    def __init__(self):
        super().__init__()

        self.filename = CONFIG_FILENAME

        self.initialized: bool = False
        self.brawl_stats_token: str or None = None
        self.discord_bot_token: str or None = None
        self.post_channel: int or None = None

    def _sync_fields(self):
        self.initialized = self.get_property('DEFAULT', 'initialized', default_value=False, cast_type=bool)
        self.brawl_stats_token = self.get_property('brawl-stats', 'token')
        self.discord_bot_token = self.get_property('discord', 'token')
        self.post_channel = self.get_property('channels', 'post_channel', cast_type=int)

    def _sync_properties(self):
        self.set_property('DEFAULT', 'initialized', self.initialized)
        self.set_property('brawl-stats', 'token', self.brawl_stats_token)
        self.set_property('discord', 'token', self.discord_bot_token)
        self.set_property('channels', 'post_channel', self.post_channel)


config = BotConfig()
config.load()

atexit.register(config.save)
