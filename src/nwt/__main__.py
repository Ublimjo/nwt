# -*- coding: utf-8 -*-
"""
Entry point of module
"""
from __future__ import division, print_function, absolute_import

from nwt import __version__
from nwt.cmd import Interactive

import click


__author__ = "Ublim"
__copyright__ = "Ublim"
__license__ = "mit"


@click.group(invoke_without_command=True)
@click.pass_context
@click.version_option()
def main(ctx):
    """
    Bible new world translation
    """
    if not ctx.invoked_subcommand:
        greet()
        workon = Interactive()
        print(workon)
        workon.run()


def greet():
    import os
    width = os.get_terminal_size()[0]
    sVersion = 'Version: ' + __version__
    title = 'bible new world translation'

    print('-' * width)
    print()
    print(title.center(width))
    print(sVersion.center(width))
    print()
    print('-' * width)
