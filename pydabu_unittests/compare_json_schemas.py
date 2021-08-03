"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-03-10, 2021-07-29
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

tests compare_json_schemas from the module dabu


You can run this file directly:

env python3 compare_json_schemas.py

Or you can run only one test, e. g.:

env python3 compare_json_schemas.py CompareJsonSchemas.test_simple_compare
"""

import unittest


# pylint: disable=invalid-name
class CompareJsonSchemas(unittest.TestCase):
    """
    :Author: Daniel Mohr
    :Date: 2021-07-29
    """

    def test_compare_list_as_set(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-07-29

        env python3 compare_json_schemas.py \
          CompareJsonSchemas.test_compare_list_as_set
        """
        # pylint: disable=bad-option-value,import-outside-toplevel
        from dabu.compare_json_schemas.compare_json_schemas \
            import compare_list_as_set, assertEqual
        compare_list_as_set([1, 2, 3], [3, 2, 1], comparefct=assertEqual)
        compare_list_as_set([1, 2, 3], [3, 2, 1])
        compare_list_as_set((1, 2, 3), (3, 2, 1))
        with self.assertRaises(AssertionError):
            compare_list_as_set([1, 2, 4], [3, 2, 1], comparefct=assertEqual)
        with self.assertRaises(AssertionError):
            compare_list_as_set([1, 2, 4], [3, 2, 1])
        with self.assertRaises(AssertionError):
            compare_list_as_set([1, 2, 3], [4, 3, 2, 1])
        with self.assertRaises(AssertionError):
            compare_list_as_set((1, 2, 3), [3, 2, 1])

    def test_simple_compare(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-03-10
        """
        # pylint: disable=bad-option-value,import-outside-toplevel
        import dabu.compare_json_schemas
        dabu.compare_json_schemas.compare_json_schemas(1, 1)
        with self.assertRaises(AssertionError):
            dabu.compare_json_schemas.compare_json_schemas(
                {0: 1}, {0: 1, 2: 3})

    def test_dict_compare(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-03-10
        """
        # pylint: disable=bad-option-value,import-outside-toplevel
        import dabu.compare_json_schemas
        a = {'b': 2, 'a': 1}
        b = {'a': 1, 'b': 2}
        dabu.compare_json_schemas.compare_json_schemas(
            a, b, comparefct=self.assertEqual)
        a = {'b': 2, 'a': 1}
        b = {'a': 1, 'b': 3}
        with self.assertRaises(AssertionError):
            dabu.compare_json_schemas.compare_json_schemas(
                a, b, comparefct=self.assertEqual)
        with self.assertRaises(AssertionError):
            dabu.compare_json_schemas.compare_json_schemas(a, b)

    def test_list_compare(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-03-10
        """
        # pylint: disable=bad-option-value,import-outside-toplevel
        import dabu.compare_json_schemas
        a = [1, 2]
        b = [2, 1]
        dabu.compare_json_schemas.compare_json_schemas(
            a, b, comparefct=self.assertEqual)

    def test_compare(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-03-10
        """
        # pylint: disable=bad-option-value,import-outside-toplevel
        import dabu.compare_json_schemas
        a = {'b': [1, 2], 'a': [{'d': 2, 'c': 1}, [3, 4]]}
        b = {'a': [[4, 3], {'c': 1, 'd': 2}], 'b': [2, 1]}
        dabu.compare_json_schemas.compare_json_schemas(
            a, b, comparefct=self.assertEqual)
        b = {'a': [[4, 4], {'c': 1, 'd': 2}], 'b': [2, 1]}
        with self.assertRaises(AssertionError):
            dabu.compare_json_schemas.compare_json_schemas(
                a, b, comparefct=self.assertEqual)
        e1 = {'b': [1, 2, {'f': 5}, [6, 7]], 'a': [{'d': 2, 'c': 1}, [3, 4]]}
        e2 = {'a': [[4, 3], {'c': 1, 'd': 2}], 'b': [2, 1, [6, 7], {'f': 5}]}
        a = {'e': e1, 'b': [1, 2, e2], 'a': [{'d': 2, 'c': 1}, [3, 4]]}
        b = {'a': [[4, 3], {'c': 1, 'd': 2}], 'b': [2, e1, 1], 'e': e2}
        dabu.compare_json_schemas.compare_json_schemas(
            a, b, comparefct=self.assertEqual)
        dabu.compare_json_schemas.compare_json_schemas(
            b, a, comparefct=self.assertEqual)
        b = {'a': [[4, 3, 6], {'c': 1, 'd': 2}], 'b': [2, e1, 1], 'e': e2}
        with self.assertRaises(AssertionError):
            dabu.compare_json_schemas.compare_json_schemas(
                a, b, comparefct=self.assertEqual)
        with self.assertRaises(AssertionError):
            dabu.compare_json_schemas.compare_json_schemas(
                b, a, comparefct=self.assertEqual)
        a = {'a': [1, {'b': 'foo', 'c': {'d': 'bar'}, 'e': [1, 2]}]}
        b = {'a': [{'b': 'foo', 'e': [1, 2], 'c': {'d': 'bar'}}, 1]}
        dabu.compare_json_schemas.compare_json_schemas(
            a, b, comparefct=self.assertEqual)
        b = {'a': [{'b': 'foo', 'e': [1, 2], 'c': {'d': 'baz'}}, 1]}
        with self.assertRaises(AssertionError):
            dabu.compare_json_schemas.compare_json_schemas(
                a, b, comparefct=self.assertEqual)
        b = {'a': [{'b': 'foo', 'e': [1, 2, 3], 'c': {'d': 'bar'}}, 1]}
        with self.assertRaises(AssertionError):
            dabu.compare_json_schemas.compare_json_schemas(
                a, b, comparefct=self.assertEqual)
        b = {'a': [{'b': 'foo', 'e': [1, 3], 'c': {'d': 'bar'}}, 1]}
        with self.assertRaises(AssertionError):
            dabu.compare_json_schemas.compare_json_schemas(
                a, b, comparefct=self.assertEqual)


if __name__ == '__main__':
    unittest.main(verbosity=2)
