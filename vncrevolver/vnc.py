from typing import Optional, Tuple
import asyncio

import aiohttp
import numpy

from asyncvnc import Client, connect

__all__ = ["check_crt_alt_del"]


class VNCClient:
    """Wrapper of vnc to check ctrl+alt+del"""

    client: Client
    host: str
    port: int

    def __init__(self, host: str, port: int):
        """
        :param host: host address
        :type host: str
        :param port: host port
        :type port: int
        """

        self.host = host
        self.port = port

    async def _get_screen(self) -> numpy.ndarray:
        return await self.client.screenshot()

    def _send_keystroke_combination(self, *keys: str) -> None:
        self.client.keyboard.press(*map(str.capitalize, keys))

    async def check_crt_alt_del(self, screen_delay: int = 2000) -> bool:
        """A function that checks if pressing the ctrl+alt+del key combination has changed the image on the screen

        :param screen_delay: delay between taking two screenshots in milliseconds
        :type screen_delay: int

        :return: Did the image on the screen change after pressing ctrl+alt+del
        :rtype: bool
        """

        result = False
        try:
            async with connect(host=self.host, port=self.port) as client:
                self.client = client

                screen_first = await self._get_screen()
                self._send_keystroke_combination('ctrl', 'alt', 'del')
                await asyncio.sleep(screen_delay / 1000)
                screen_second = await self._get_screen()

                result = bool((screen_first != screen_second).all())

        except Exception as e:
            from asyncio.exceptions import __all__ as asyncio_exceptions

            er = (str(e.__class__) + str(e.args)).lower()
            if "password" in er or "connect" in er or isinstance(e, (EnvironmentError, ValueError, PermissionError)) \
                    or str(e.__class__.__name__) in asyncio_exceptions:
                """
                ..note::
                    This is not shitcode, it's just that there is no general exception in the library
                    Ok, this is shitcode, but I didn't find a proper way to except the server connection or timeout error >:(
                """
                pass
            else:
                raise e

        return result


async def check_crt_alt_del(host: str, port: int, screen_delay: int = 2000):
    """A function that checks if pressing the ctrl+alt+del key combination has changed the image on the screen


    :param host: host address
    :type host: str
    :param port: host port
    :type port: int
    :param screen_delay: delay between taking two screenshots in milliseconds
    :type screen_delay: int

    :return: Did the image on the screen change after pressing ctrl+alt+del
    :rtype: bool
    """

    vnc = VNCClient(host=host, port=port)
    try:
        r = await asyncio.wait_for(vnc.check_crt_alt_del(screen_delay=screen_delay), timeout=screen_delay/1000*2.5)
        return r
    except asyncio.TimeoutError:
        return False
