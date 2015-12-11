import unittest


from telegrambot import cli


class TestConfigDict(unittest.TestCase):
    def test_configdict_get_attr(self):
        cfg = cli.ConfigDict(a=1)
        self.assertEqual(cfg.a, 1)
        self.assertEqual(cfg['a'], 1)

    def test_configdict_get_noattr(self):
        cfg = cli.ConfigDict()
        self.assertEqual(cfg.a, None)

    def test_configdict_set_attr(self):
        cfg = cli.ConfigDict(a=1)
        cfg.b = 2
        self.assertEqual(cfg.a, 1)
        self.assertEqual(cfg.b, 2)

    def test_configdict_comparison(self):
        cfg1 = cli.ConfigDict(a=1)
        cfg2 = cli.ConfigDict(a=1)
        self.assertDictEqual(cfg1, cfg2)


class TestCliMain(unittest.TestCase):
    pass