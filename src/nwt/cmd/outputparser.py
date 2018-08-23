"""
Module to output and render to terminal or another stdout
"""
import textwrap

import attr
from bs4 import BeautifulSoup, NavigableString

from nwt.cmd.fileparser import bookList
from nwt.cmd.inputparser import InputParser
from nwt.utils import color


def between(cur, end):
    while cur and cur != end:
        if isinstance(cur, NavigableString):
            text = cur.strip()
            if len(text):
                yield text
        cur = cur.next_element


def wrap(string, indent=0):
    text = textwrap.wrap(string, 60)
    line = "\n" + (' ' * indent) + color.green(" | ")
    final = line.join(text) + line
    return final


class Render(object):
    '''
    obj
    ---
    { 'matio': {
        '24': {
            '14': 'Ary hotoriana',
            '15': 'noho izany',
            '16': 'dia aoka izay',
        }
    }
    output
    ------
    Matio 24 14 Ary hotorina maneran-tany ity vaovao tsaran’ilay
           |  | fanjakana ity, ho vavolombelona amin’ny firenena rehetra,
           |  | vao ho tonga ny farany.
           | 15 noho izany
           | 16 dia aoka izany
    '''

    def __init__(self, obj):
        self.text = ''
        for book in obj:
            self.text += '{} '.format(color.blue(book.title()))
            lenbook = len(book)
            for chapter in obj[book]:
                self.text += '{} '.format(color.green(chapter))
                lenchapter = len(str(chapter))
                for verset in obj[book][chapter]:
                    self.text += '{} '.format(color.red(verset))
                    lenverset = len(str(verset))
                    wtext = textwrap.wrap(obj[book][chapter][verset], 60)
                    for line in wtext:
                        self.text += (line + '\n' + (' ' * (lenbook +
                                                            lenchapter)) + color.green('|') + (' ' * lenverset) +
                                      color.red('|') + ' ')
                    self.text += ('\n' + (' ' * (lenbook + lenchapter)) +
                                  color.green('|') + ' ')
                self.text += ('\n' + (' ' * (lenbook + lenchapter)))

    def __str__(self):
        return self.text


@attr.s
class OutputParser(object):
    query = attr.ib()
    text = attr.ib('')

    def __attrs_post_init__(self):
        if not isinstance(self.query, InputParser):
            raise ValueError('query must be InputParser obj')
        self.query = self.query.result
        rendered = self.query

        for book in self.query:
            for chapter in self.query[book]:
                bfile = bookList[book][str(chapter)]
                with open(bfile, 'r') as fp:
                    soup = BeautifulSoup(fp, "html.parser")
                for verset in self.query[book][chapter]:
                    start = u"chapter" + str(chapter) + "_verse" + str(verset)
                    end = u"chapter" + str(chapter) + \
                        "_verse" + str(verset + 1)
                    try:
                        rendered[book][chapter][verset] = ' '.join(_ for _ in between(
                            soup.find("span", attrs={
                                      "id": start}).next_sibling,
                            soup.find("span", attrs={"id": end})))
                    except AttributeError:
                        rendered[book][chapter][verset] = 'Invalid verset'
        self.text = Render(rendered)

    def __str__(self):
        return str(self.text)
