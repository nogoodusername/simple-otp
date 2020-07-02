"""Top-level package for simple-otp."""

__author__ = """Kshitij Nagvekar"""
__email__ = 'kshitij.nagvekar@workindia.in'
__version__ = '0.1.0'

try:
    from secrets import SystemRandom
except ImportError:
    from random import SystemRandom

from typing import Sequence
from .otp import OTP

random = SystemRandom()


def generate_secret(
    length: int = 16,
    chars: Sequence[str] = None
) -> str:
    """
    Generates a secret which can be used as secret key
    :param length: key length
    :param chars: list of characters to be used to generate secret key
    :return: secret key string
    """

    if chars is None:
        chars = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')

    return ''.join(
        random.choice(chars)
        for _ in range(length)
    )


__all__ = ["generate_secret", "OTP"]
