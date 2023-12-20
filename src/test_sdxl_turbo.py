import unittest

from sdxl_turbo import SdxlQuery, SdxlTurbo
from io import BytesIO

class TestSdxlQuery(unittest.TestCase):

    def test_init(self):
        prompt = "prompt"

        query = SdxlQuery(prompt)
        self.assertEqual(query.main_prompt, prompt)

    def test_get_full_prompt_with_tags(self):
        prompt = "prompt"
        tags = ["2d"]
        expected = "prompt, 2d"

        query = SdxlQuery(prompt)
        query.tags = tags

        self.assertEqual(query.get_full_prompt(), expected)

    def test_get_full_prompt_without_tags(self):
        prompt = "prompt"

        query = SdxlQuery(prompt)
        query.tags = []

        self.assertEqual(query.get_full_prompt(), prompt)

    def test_add_tag(self):
        new_tag = "tag"

        query = SdxlQuery("")
        before_add_tag_len = len(query.tags)
        query.add_tag(new_tag)

        self.assertEqual(len(query.tags), before_add_tag_len + 1)
        self.assertEqual(query.tags[-1], new_tag)

    def test_remove_tag(self):
        tag = "2d"

        query = SdxlQuery("")
        query.tags = [tag]
        result = query.try_remove_tag(tag)

        self.assertTrue(result)
        self.assertEqual(len(query.tags), 0)

    def test_remove_last_tag(self):
        query = SdxlQuery("")
        last_tag = query.tags[-1]

        result = query.try_remove_last_tag()

        self.assertTrue(result)
        self.assertNotEqual(last_tag, query.tags[-1])

class TestSdxlTurbo(unittest.TestCase):
    
    def test_generate(self):
        query = SdxlQuery("")
        model = SdxlTurbo()

        result = model.generate(query)

        self.assertIsInstance(result, BytesIO)

if __name__ == '__main__':
    unittest.main()