"""
A series of utility functions for YAEP
"""


def str_to_bool(string, boolean_map=None):
    if not boolean_map:
        boolean_map = {
            True: ['True', '1'],
            False: ['False', '0']
        }

    for boolean in boolean_map:
        if any(string.lower() == val.lower() for val in boolean_map[boolean]):
            return boolean

    return string


class SectionHeader(object):
    header = 'dummy'

    def __init__(self, fp):
        self.fp = fp
        self.sent_header = False

    def readline(self):
        if not self.sent_header:
            self.sent_header = True
            read_data = '[{}]\n'.format(self.header)
        else:
            read_data = self.fp.readline()

        return read_data
