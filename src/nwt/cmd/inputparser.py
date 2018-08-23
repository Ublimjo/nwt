import collections

from nwt.utils import GetDistance


def _int(castable):
    try:
        return int(castable)
    except ValueError:
        return castable


def unpack(packed):
    first = int(packed.split('-')[0])
    second = int(packed.split('-')[1])
    if first == second:
        return first
    if not first < second:
        first, second = second, first
    unpacked = [first]
    while first < second:
        first += 1
        unpacked.append(first)
    return unpacked


def flatten(inputArr, outputArr=None, isFirst=True):
    if not outputArr and isFirst:
        outputArr = []
    for ele in inputArr:
        if isinstance(ele, collections.Iterable):
            flatten(ele, outputArr, False)
        else:
            outputArr.append(ele)
    return outputArr


def entry(_list):
    _dict = {}
    for index in _list:
        _dict[index] = ''
    return _dict


class InputParser(object):
    def __init__(self, query):
        self.query = query
        self.isValid = False
        self.result = {}

        def parse():
            pbook = self.query.lower().split(' ')
            prebook1 = GetDistance(pbook[0])
            prebook2 = GetDistance(pbook[0] + ' ' + pbook[1])

            if prebook1.distance < prebook2.distance:
                entbook = prebook1
                with_sub = False
            if prebook1.distance > prebook2.distance:
                entbook = prebook2
                with_sub = True
            if prebook1.distance == prebook2.distance:
                entbook = prebook1
                if len(prebook1.closest.split(' ')) == 1:
                    with_sub = True
                else:
                    with_sub = False

            rawsubbook = pbook[1] if not with_sub else pbook[2]
            subbook = {}
            for raw in rawsubbook.split(';'):
                chapter = int(raw.split(':')[0])
                verset = list(_int(item) for item in
                              raw.split(':')[1].split(','))
                subbook[chapter] = verset

            for chapter in subbook:
                workon = subbook[chapter]
                for i, lsvt in enumerate(workon):
                    if "-" in str(lsvt):
                        del workon[i]
                        workon.insert(i, unpack(lsvt))
                subbook[chapter] = entry(flatten(workon))
            self.result = {}
            self.result[entbook.closest] = subbook

        parse()

    def __str__(self):
        _str = ''
        for book in self.result:
            _str += (book + ' ')
            for chapter in self.result[book]:
                _str += (str(chapter) + ':')
                for verset in self.result[book][chapter]:
                    _str += (str(verset) + ',')
                _str = _str[:-1]
                _str += ';'
            _str = _str[:-1]
        return _str

    def __repr__(self):
        return repr(self.result)

    def __len__(self):
        _len = 0
        for book in self.result:
            for chapter in self.result[book]:
                for verset in self.result[book][chapter]:
                    _len += 1
        return _len
