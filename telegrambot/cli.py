import argparse
import ConfigParser

from telegrambot.bot import TelegramBot


class ConfigDict(dict):
    def __getattr__(self, name):
        return self.get(name)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('config')
    args = parser.parse_args()

    cfg = ConfigDict()
    cfg_parser = ConfigParser.ConfigParser()
    cfg_parser.read(args.config)
    for section in cfg_parser.sections():
        cfg[section] = ConfigDict(cfg_parser.items(section))
    if 'plugins' in cfg.core:
        cfg.core.plugins = cfg.core.plugins.split(',')
    else:
        cfg.core.plugins = None  # paradoxically, this means all plugins
    bot = TelegramBot(cfg)
    bot.loop()


if __name__ == '__main__':
    main()
