from nwt.cmd.inputparser import InputParser


def test_InputParser():
    query = InputParser('1 jaOner 2:1-3,5;4:7,9-12')
    assert query.result == {'1 Jaona': {
            2: {1: '',2: '',3: '',5: ''},
            4: {7: '',9: '',10: '',11: '', 12: ''},
    }}
