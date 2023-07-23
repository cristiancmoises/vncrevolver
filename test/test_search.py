from typing import List
import unittest

from vncrevolver.search import VNC, search_random, search_filter


class SearchRandomTest(unittest.IsolatedAsyncioTestCase):
    async def test_search_random(self):
        await search_random()


class SearchFilterTest(unittest.IsolatedAsyncioTestCase):
    async def test_search_filter(self):
        await search_filter(clientname='e')

    async def test_without_parameters(self):
        with self.assertRaises(AssertionError):
            await search_filter()


if __name__ == '__main__':
    unittest.main()
