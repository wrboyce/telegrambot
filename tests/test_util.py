import unittest
import uuid

from telegrambot import util


class TestUtil(unittest.TestCase):
    def test_is_int(self):
        self.assertTrue(util.is_int(0))
        self.assertTrue(util.is_int(1))
        self.assertTrue(util.is_int(1000))
        self.assertTrue(util.is_int('0'))
        self.assertFalse(util.is_int('one'))
        self.assertFalse(util.is_int('1,000'))

    def test_humanize_int_0(self):
        self.assertEqual('0', util.humanize_int(0))

    def test_humanize_int_1_to_9(self):
        self.assertEqual('one', util.humanize_int(1))
        self.assertEqual('nine', util.humanize_int(9))

    def test_humanize_int_10_to_999(self):
        self.assertEqual('10', util.humanize_int(10))
        self.assertEqual('999', util.humanize_int(999))

    def test_humanize_int_1000_to_999999(self):
        self.assertEqual('1,000', util.humanize_int(1000))
        self.assertEqual('999,999', util.humanize_int(999999))

    def test_humanize_int_1_million_plus(self):
        self.assertEqual('1.0 million', util.humanize_int('1000000'))
        self.assertEqual('1.0 billion', util.humanize_int('1000000000'))

    def test_is_image(self):
        img_exts = ('.jpg', '.jpeg', '.gif', '.png', '.tif', '.bmp')
        gen_filename = lambda ext: '/dev/null/{}{}'.format(uuid.uuid4(), ext)
        for ext in img_exts:
            fn = gen_filename(ext)
            self.assertTrue(util.is_image(fn))

    def test_is_image_case_insensitive(self):
        img_exts = ('.jpg', '.jpeg', '.gif', '.png', '.tif', '.bmp')
        gen_filename = lambda ext: '/dev/null/{}{}'.format(uuid.uuid4(), ext)
        for ext in img_exts:
            fn = gen_filename(ext.upper())
            self.assertTrue(util.is_image(fn))

    def test_is_image_no_extension(self):
        fn = '/dev/null/{}'.format(uuid.uuid4())
        self.assertFalse(util.is_image(fn))
