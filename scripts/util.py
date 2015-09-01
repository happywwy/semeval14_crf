

import itertools


def paragraphs(source, separator = "\n"):
    ''' Iterate over source by paragraph'''
    lines = []
    for line in source:
        if line == separator and lines:
            yield ''.join(lines)
            lines = []
        else:
            lines.append(line)
    if lines:
        yield ''.join(lines)
