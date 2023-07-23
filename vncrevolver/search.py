from typing import Optional, Iterable, Union, List, Dict
from datetime import datetime

from pydantic import BaseModel

from . import http_api

__all__ = ["VNC", "search_filter", "search_random"]


class VNC(BaseModel):
    """VNC information object

    :param id: is the Scan ID of the VNC. This is unique to this VNC, and this particular scan.
    :type id: int
    :param ip: is the IP Address of the VNC.
    :type ip: str
    :param port: is the port number the VNC is listening on.
    :type port: int
    :param city: is the approximate city the VNC is located in.
    :type city: str
    :param state: is the approximate state the VNC is located in.
    :type state: str
    :param country: is the country the VNC is located in.
    :type country: str
    :param clientname: is the desktop name the VNC sent when the scan was taken.
    :type clientname: str
    :param screenres: is the screen resolution the VNC was at when the scan was taken.
    :type screenres: str
    :param hostname: is the rDNS hostname of the VNC.
    :type hostname: Union[str, None]
    :param osname: is the OS the VNC is running when the scan was taken (probed by nmap, so results may be a little inaccurate)
    :type osname: str
    :param openports: is the open ports on the VNC.
    :type openports: List[int]
    :param username: is the username required to log in to the VNC when the scan was taken.
    :type username: str
    :param password: is the password required to log in to the VNC when the scan was taken.
    :type password: str
    :param createdat: is when the VNC was added to the Resolver database.
    :type createdat: datetime
    :param asn: is autonomous system number on which the VNS is located.
    :type asn: str
    """

    id: int
    ip: str
    port: int
    city: str
    state: str
    country: str
    clientname: str
    screenres: str
    hostname: Union[str, None]
    osname: str
    openports: Iterable[int]
    username: str
    password: str
    createdat: datetime
    asn: str


async def search_filter(
        clientname: Optional[str] = None,
        country: Optional[str] = None,
        asn: Optional[str] = None,
) -> List[VNC]:
    """Search several VNC by filtering

    :param clientname: filter by client name, note that it is case-sensitive!
    :type clientname: Optional[str]
    :param country: filter by ISO 3166-1 alpha-2 country code
    :type country: Optional[str]
    :param asn: filter by ASN
    :type asn: Optional[str]

    :return: information about each found host
    :rtype: List[VNC]
    """

    results: List[http_api.VNCInfo] = await http_api.search_filter(clientname=clientname, country=country, asn=asn)

    return [VNC(**x) for x in results]  # type: ignore


async def search_random() -> VNC:
    """Getting random VNC

    :return: dict with full information
    :rtype: VNCObject
    """

    results: http_api.VNCInfo = await http_api.search_random()

    return VNC(**results)  # type: ignore
