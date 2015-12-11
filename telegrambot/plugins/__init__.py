"""
    Copyright 2015 Will Boyce

    There is some magic below to handle importing everything defined under telegrambot.plugins
    so the plugin registry can be populated.
"""
import pkgutil


__path__ = pkgutil.extend_path(__path__, __name__)
for loader, module_path, is_pkg in pkgutil.walk_packages(__path__):
    loader.find_module(module_path).load_module(module_path)
