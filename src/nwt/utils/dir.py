import os

from nwt.utils.path import Path


class Dir(object):
    prefix = Path(os.environ['PREFIX'])
    home = Path(os.path.expanduser('~'))

    sysDir = prefix / 'share' / 'nwt/'
    homeDir = home / '.nwt/'

    bookDir = homeDir / 'book/'
    tmpRoot = bookDir / 'bi12_MG' / 'OEBPS/'
