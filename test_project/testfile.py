#!/usr/bin/python

# this is a demo file, just for testing doctester.py


class A(object):
    """
    >>> a = A(4)
    >>> a.boo()
    >>> a.boo()
    >>> a.val == 16
    True
    """
    def __init__(self, val):
        self.val = val

    def boo(self):
        self.val *= 2


def main():
    """
    >>> main()
    32
    """
    b = A(16)
    b.boo()
    return b.val


if __name__ == '__main__':
    main()
