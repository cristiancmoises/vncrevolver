import asyncio
import unittest

from vncrevolver.search import VNC, search_random
from vncrevolver.vnc import check_crt_alt_del


class MyTestCase(unittest.IsolatedAsyncioTestCase):
    async def _test(self, host):
        self.assertIsInstance(await check_crt_alt_del(host=host.ip, port=host.port), bool)

    async def test_check_crt_alt_del(self):
        tasks = map(_test, [await search_random() for _ in range(10)])
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    unittest.main()
