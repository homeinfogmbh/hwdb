"""Terminal database query utility."""

from logging import DEBUG, INFO, basicConfig, getLogger

from b64lzma import B64LZMA

from hwdb.config import LOG_FORMAT
from hwdb.hwutil.argparse import get_args
from hwdb.hwutil.deployment import find as find_deployment
from hwdb.hwutil.deployment import list as list_deployments
from hwdb.hwutil.system import find as find_system
from hwdb.hwutil.system import list as list_systems


__all__ = ['main']


ARNIE = B64LZMA(
    '/Td6WFoAAATm1rRGAgAhARYAAAB0L+Wj4AIEAK9dABBuADwUaYt0gRsna7sph26BXekoRMls4'
    'PqOjQ0VHvqxoXly1uRgtvfLn9pvnm1DrCgcJiPp8HhWiGzH7ssJqMiSKm0l67Why5BVT8apzO'
    'CVXevyza2ZXmT21h0aDCiPYjN4ltUrrguxqC4Lwn0XwvoWRxpXGb0wAyV//ppegMFpCqvR3y/'
    'l6gnu1zzfCVOISaOCOjHXq2NiJ3ZUMv76UcKZjfFEnW11r/P35yFKGo4AAJxj7ZVSD0rZAAHL'
    'AYUEAADP/ZRYscRn+wIAAAAABFla'
)
LOGGER = getLogger('hwutil')


def main() -> int:
    """Runs the system utility."""

    args = get_args()
    basicConfig(level=DEBUG if args.verbose else INFO, format=LOG_FORMAT)
    success = False

    if args.action == 'ls':
        if args.target == 'sys':
            success = list_systems(args)
        elif args.target == 'dep':
            success = list_deployments(args)
    elif args.action == 'find':
        if args.target == 'sys':
            success = find_system(args)
        elif args.target == 'dep':
            success = find_deployment(args)
    elif args.action == 'CSM-101':
        print(ARNIE)
        success = True

    return 0 if success else 1
