import attr
from .pylev import damerau_levenshtein as lev

from .dir import Dir
from nwt.data import bookList as book_list


@attr.s
class GetDistance(object):
    enter = attr.ib('')
    closest = attr.ib('', init=False)
    distance = attr.ib(0, init=False)

    def __attrs_post_init__(self):
        dist_list = []
        for book in book_list:
            dist_list.append(lev(book, self.enter))

        while True:
            try:
                self.closest = book_list[dist_list.index(self.distance)]
                break
            except ValueError:
                self.distance += 1
