from typing import Optional, Iterable, List, Dict, Tuple
from dataclasses import dataclass

import aiohttp

__all__ = ["VNCInfo", "search_filter", "search_random", "ApiRequestFailed"]

VNCInfo = Dict[str, str]


@dataclass
class ApiRequestFailed(Exception):
    """Thrown if the computernewb.com API server response code is != 20x"""

    status_code: int
    url: str
    response_text: str

    def __str__(self):
        return "Status code: {}\nUrl: {}\nResponse text: {}".format(self.status_code, self.url, self.response_text)


def _remove_duplicates(vncs: Iterable[VNCInfo]) -> List[VNCInfo]:
    """Removes duplicate hosts from the dictionary, targeting the max field ``createdat``, ``ip`` and ``id`` as an idifier

    :param vncs: List of dictionaries to sort
    :type vncs: Iterable[VNCInfo]

    :return: Sorted list of dictionaries without duplicates
    :rtype: List[VNCInfo]

    Example:

        .. code-block:: python

        >>> a = [
                {'id': 1, 'createdat': 1, 'ip': '0.0.0.0'},
                {'id': 2, 'createdat': 2, 'ip': '0.0.0.0'},
                {'id': 3, 'createdat': 1, 'ip': '0.0.0.1'}
            ]
        >>> pprint(remove_duplicates(a))
        [{'id': 2, 'createdat': 2, 'ip': '0.0.0.0'},
        {'id': 3, 'createdat': 1, 'ip': '0.0.0.1'}]

    """

    unique_vns: Dict[str, Tuple[float, int]] = {}

    for result in vncs:
        if float(result['createdat']) > float(unique_vns.get(result["ip"], (0, 0))[0]):
            unique_vns[result['ip']] = float(result['createdat']), int(result['id'])

    unique_id = list(map(lambda vnc: vnc[1], unique_vns.values()))

    results = list(filter(lambda vnc: vnc['id'] in unique_id, vncs))

    return results


async def search_filter(
        clientname: Optional[str] = None,
        country: Optional[str] = None,
        asn: Optional[str] = None
) -> List[VNCInfo]:
    """Search several VNC by filtering through the computernewb.com API

    :param clientname: filter by client name, note that it is case-sensitive!
    :type clientname: Optional[str]
    :param country: filter by ISO 3166-1 alpha-2 country code
    :type country: Optional[str]
    :param asn: filter by ASN
    :type asn: Optional[str]

    :return: information about each found VNCs
    :rtype: List[VNCInfo]

    :exception ApiRequestFailed: Thrown if the computernewb.com API server response code is != 20x
    :exception AssertionError: Thrown if no parameters for filtering are specified
    """

    params = {"full": "true"}

    if clientname:
        params["clientname"] = clientname

    if country:
        params["country"] = country

    if asn:
        params["asn"] = asn

    assert len(params) > 1, "You must specify at least one parameter for filtering"

    async with aiohttp.ClientSession() as session:
        async with session.get("https://computernewb.com/vncresolver/api/scans/vnc/search", params=params) as response:

            if not response.ok:
                raise ApiRequestFailed(status_code=response.status, url=response.url, response_text=await response.text())

            results: List[VNCInfo] = (await response.json())['result']

            results = _remove_duplicates(results)

            return results


async def search_random() -> VNCInfo:
    """Getting random VNC through the computernewb.com API

    :return: dict with full information about found VNC
    :rtype: VNCInfo

    :exception ApiRequestFailed: Thrown if the computernewb.com API server response code is != 20x
    """

    async with aiohttp.ClientSession() as session:
        async with session.get("https://computernewb.com/vncresolver/api/scans/vnc/random") as response:

            if not response.ok:
                raise ApiRequestFailed(status_code=response.status, url=response.url, response_text=await response.text())

            result: VNCInfo = await response.json()

            return result
