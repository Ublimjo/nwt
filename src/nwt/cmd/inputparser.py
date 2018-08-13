from icecream import ic
import attr
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


@attr.s
class InputParser(object):
    query = attr.ib('')
    isValid = attr.ib(False)
    result = attr.ib({})

    def __attrs_post_init__(self):
        def parse(self):
            pbook = self.query.lower().split(' ')
            prebook1 = GetDistance(pbook[0])
            prebook2 = GetDistance(pbook[0] + ' ' + pbook[1])

            if prebook1.distance < prebook2.distance:
                entbook = prebook1
                with_sub = False
            if prebook1.distance > prebook2.distance:
                entbook = prebook2
                with_sub = True

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
                subbook[chapter] = flatten(workon)
            self.result[entbook.closest] = subbook

        parse(self)
