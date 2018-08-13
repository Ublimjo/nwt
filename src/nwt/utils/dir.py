import os

from nwt.utils.path import Path


class Dir(object):
    prefix = Path(os.environ['PREFIX'])
    home = Path(os.path.expanduser('~'))

    sysDir = prefix / 'share' / 'nwt/'
    homeDir = home / '.nwt/'

    bookDir = sysDir / 'book/'
    tmpRoot = bookDir / 'nwt_E' / 'OEBPS/'
