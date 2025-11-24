# tests.py
from converter import NumberConverter
import unittest

class TestConverter(unittest.TestCase):
    def setUp(self):
        self.c = NumberConverter()

    def test_pdf_cases(self):
        # Test case: 536 -> five hundred and thirty-six
        self.assertEqual(self.c.process_sentence("The pump is 536 deep underground."), 
                         "five hundred and thirty-six")
        
        # Test case: 9121 -> nine thousand, one hundred and twenty-one
        self.assertEqual(self.c.process_sentence("We processed 9121 records."), 
                         "nine thousand, one hundred and twenty-one")
                         
        # Test case: Invalid #65678
        self.assertEqual(self.c.process_sentence("Variables reported as having a missing type #65678."), 
                         "number invalid")
                         
        # Test case: Large number
        self.assertEqual(self.c.process_sentence("66723107008"), 
                         "sixty-six billion, seven hundred and twenty-three million, one hundred and seven thousand and eight")

if __name__ == '__main__':
    unittest.main()
