# -*- coding: utf-8 -*-
"""
module for entry interaction
"""
import sys
import attr
from prompt_toolkit import prompt

from .inputparser import InputParser
from .outputparser import OutputParser


@attr.s
class Interactive(object):
    state = attr.ib({
        'main': 'nwt',
        'book': '',
        'chapter': 0,
        'verset': 0})
    on = attr.ib(default='main')
    lprompt = attr.ib()

    @on.validator
    def check(self, attribute, value):
        if value not in self.state.keys():
            raise ValueError("on must be in state keys")

    @lprompt.default
    def lp__init__(self):
        """
        Set left prompt
        """
        if not self.state['book']:
            self.on = 'main'
            return ' {} > '.format(
                self.state['main'])
        if not self.state['chapter']:
            self.on = 'book'
            return ' {} > {} > '.format(
                self.state['main'],
                self.state['book'])
        if not self.state['verset']:
            self.on = 'chapter'
            return ' {} > {} > {} > '.format(
                self.state['main'],
                self.state['book'],
                self.state['chapter'])

    def prompter(self):
        """
        Function to replace 'input', 'prompt'
        """
        try:
            self.lprompt = self.lp__init__()
            result = prompt(self.lprompt)
            return result
        except (KeyboardInterrupt, EOFError):
            sys.exit(0)

    def run(self):
        """
        Run interactive session here
        """
        while True:
            query = self.prompter().lower().split(' ')
            # if (len(query) == 1):
            #     if (self.on == 'main'):
            #         self.state['book'] = query[0]
            #     if (self.on == 'book'):
            #         self.state['chapter'] = query[0]
            parsed = InputParser(' '.join(query))
            text = OutputParser(parsed)
            print(text)
