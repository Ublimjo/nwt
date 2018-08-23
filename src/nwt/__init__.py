# -*- coding: utf-8 -*-
"""
Bible new world translation in cli
"""

from pkg_resources import get_distribution, DistributionNotFound

try:
    DIST_NAME = __name__
    __version__ = get_distribution(DIST_NAME).version
except DistributionNotFound:
    __version__ = 'unknown'
