from bs4 import BeautifulSoup

from nwt.utils import Dir

with open(Dir.tmpRoot / 'toc.xhtml', 'r') as toc:
    soup = BeautifulSoup(toc, "html.parser")

title = soup.head.title.text
rawlist = soup.body.section.nav.ol.find_all('a')[1:133]

bookList = {}
for element in rawlist:
    if not ('Outline' in element.text):
        with open(Dir.tmpRoot / element.attrs['href'], 'r') as _:
            versetp = BeautifulSoup(_, 'html.parser')
            versetList = {}
            try:
                versetp = versetp.body.table.find_all('a')
                for line in versetp:
                    fp = Dir.tmpRoot / line.attrs['href']
                    versetList[line.text] = fp
            except AttributeError:
                versetList = Dir.tmpRoot / element.attrs['href']

        bookList[element.text] = versetList
