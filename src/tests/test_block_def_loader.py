import unittest
from block_def_loader import load_block_defs
import os

class TestBlockDefLoader(unittest.TestCase):
    def test_load_yaml(self):
        path = os.path.join(os.path.dirname(__file__), '../../block-defs.yaml')
        defs = load_block_defs(path)
        self.assertIn('heading', defs)

if __name__ == '__main__':
    unittest.main()
