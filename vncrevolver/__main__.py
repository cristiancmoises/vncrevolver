from typing import Union
import asyncio
from argparse import ArgumentParser

from vncrevolver.search import search_filter, search_random
from vncrevolver.vnc import check_crt_alt_del

argparser = ArgumentParser(prog="vncrevolver",
                           epilog="""
If you specify one of the filtering parameters, a search by fitration will be launched, otherwise a search for random VNCs will be launched.
If you specify the --count option, the required VNC number will be found.
The number of found VNCs may be less than the --count parameter when searching with filtering.
""")

argparser.add_argument("--clientname", type=str, help="Filter by client name, note that it is case-sensitive!")
argparser.add_argument("--country", type=str, help="Filter by ISO 3166-1 alpha-2 country code")
argparser.add_argument("--asn", type=str, help="Filter by ASN")

argparser.add_argument("--count", type=int, default=1, help="Number of VNCs to find")

argparser.add_argument("--check_crt_alt_del", type=str, nargs='?', const=True, default=False, help="""
If you specify this parameter without a value, only those VNCs from the search that pass the ctrl_alt_del check will be returned.
If a value is passed, it must be a VNC address that will be checked against ctrl_alt_del.
""")
argparser.add_argument("--show_failed", action="store_true", help="Return VNCs that failed the ctrl_alt_del check")

argparser.add_argument("--screen_delay", default=2000, type=int, help="Delay between taking two screenshots in milliseconds")


async def _check_vnc(ip: str, port: int, screen_delay: int, failed: bool):
    r = await check_crt_alt_del(ip, port, screen_delay=screen_delay)
    if r:
        print(f"{ip}:{port}", True)
    elif failed:
        print(f"{ip}:{port}", False)


async def main():
    args = argparser.parse_args()

    hosts: List[Tuple[str, int]] = []  # [(host, port), ...]

    # creating a list with hosts & ports
    if isinstance(args.check_crt_alt_del, str):  # the host is specified in the parameters
        ip, port = args.check_crt_alt_del.__add__(":5900").split(":")[:2]
        hosts = [(ip, int(port))]
        args.check_crt_alt_del = True
    else:  # the host is NOT specified in the parameters
        if args.clientname or args.country or args.asn:  # filtering enabled
            hosts = [(vnc.ip, vnc.port) for vnc in
                     await search_filter(clientname=args.clientname, country=args.country, asn=args.asn)][:args.count]
        else:  # filtering NOT enabled
            hosts = [((vnc := await search_random()).ip, vnc.port) for _ in range(args.count)]

    if args.check_crt_alt_del:  # check mode enabled
        tasks = map(
            _check_vnc,
            [host for host, port in hosts],
            [port for host, port in hosts],
            [args.screen_delay for _ in hosts],
            [args.show_failed for _ in hosts]
        )

        await asyncio.gather(*tasks)
    else:  # check mode NOT enabled
        for host, port in hosts:
            print(f"{host}:{port}")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
