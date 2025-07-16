import unittest
from converter import convert_markdown_to_gutenberg

class TestConverter(unittest.TestCase):
    def test_heading(self):
        block_defs = {'heading': {'pattern': '<!-- wp:heading -->\n{content}\n<!-- /wp:heading -->'}}
        md = '# 見出し'
        result = convert_markdown_to_gutenberg(md, block_defs)
        self.assertIn('<!-- wp:heading -->', result)

if __name__ == '__main__':
    unittest.main()
