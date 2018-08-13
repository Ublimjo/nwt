import attr
from icecream import ic
from bs4 import BeautifulSoup

from nwt.cmd.inputparser import InputParser
from nwt.cmd.fileparser import bookList


@attr.s
class OutputParser(object):
    query = attr.ib()
    text = attr.ib('')

    def __attrs_post_init__(self):
        if not isinstance(self.query, InputParser):
            raise ValueError('query must be InputParser obj')
        self.query = self.query.result

        for book in self.query:
            self.text += '{}\n'.format(book)
            for chapter in self.query[book]:
                self.text += '{} '.format(chapter)
                bfile = bookList[book][str(chapter)]
                with open(bfile, 'r') as fp:
                    soup = BeautifulSoup(fp, "html.parser")
                for verset in self.query[book][chapter]:
                    tag = u"chapter" + str(chapter) + "_verse" + str(verset)
                    try:
                        self.text += soup.find(
                            "span", attrs={"id": tag}).next.next.next.next
                    except AttributeError:
                        self.text += 'invalid verset'

    def __str__(self):
        return self.text
