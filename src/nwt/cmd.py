# -*- coding: utf-8 -*-
"""
module for entry interaction
"""
import sys
import attr
from prompt_toolkit import prompt


@attr.s
class Interactive(object):
    state = attr.ib({
        'main': 'nwt',
        'book': 'genesisy',
        'chapter': 0,
        'verset': 0})
    lprompt = attr.ib()

    @lprompt.default
    def lp__init__(self):
        if not self.state['book']:
            return ' {} > '.format(
                self.state['main'])
        if not self.state['chapter']:
            return ' {} > {} > '.format(
                self.state['main'],
                self.state['book'])
        if not self.state['chapter']:
            return ' {} > {} > {} > '.format(
                self.state['main'],
                self.state['book'],
                self.state['chapter'])
        if not self.state['verset']:
            return ' {} > {} > {} > {} > '.format(
                self.state['main'],
                self.state['book'],
                self.state['chapter'],
                self.state['verset'])

    def prompter(self):
        try:
            result = prompt(
                self.lprompt,
                mouse_support=True)
            return result
        except (KeyboardInterrupt, EOFError):
            sys.exit(0)

    def run(self):
        while True:
            query = self.prompter()
            print(query)
