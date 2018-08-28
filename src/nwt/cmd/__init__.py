# -*- coding: utf-8 -*-
"""
module for entry interaction
"""

import sys
import attr
from prompt_toolkit import prompt, PromptSession
from prompt_toolkit.key_binding import KeyBindings

from .inputparser import InputParser
from .outputparser import OutputParser

from nwt.utils import GetDistance


class Interactive(object):
    """
    Interactive command session
    """

    def __init__(self):
        self.leftp = ' nwt > '
        self.session = PromptSession()
        self.bindings = KeyBindings()

        @self.bindings.add(' ')
        def _(event):
            b = event.app.current_buffer
            w = b.document.get_word_before_cursor()
            if w is not None:
                if len(w) > 1:
                    b.delete_before_cursor(count=99)
                    b.insert_text(GetDistance(w).closest + ' ')
                else:
                    b.insert_text(' ')

    def prompter(self):
        """
        Function to replace 'input' -> 'prompt'
        """

        try:
            result = self.session.prompt(
                self.leftp,
                key_bindings=self.bindings,
            )
            return result
        except (KeyboardInterrupt, EOFError):
            sys.exit(0)

    def run(self):
        """
        Run interactive session
        """

        while True:
            query = self.prompter().lower()
            parsed = InputParser(query)
            text = OutputParser(parsed)
            print(text)
