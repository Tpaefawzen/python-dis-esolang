"""
Implementation of esoteric language Dis, Malbolge's wimpmode
"""

import sys

_VALID_COMMANDS = "*^>|}{!_"
_COMMENT_BEGIN = "("
_COMMENT_END = ")"
_MAX_CELLS = 59049

class Dis:
    """
    Virtual machine for Dis language.
    """

    def __init__(self, src: str) -> None:
        """
        Interpret given Dis program source to load.
        """

        self.__mem: list[int] = []

        while src:
            c, *src = src
            if c in _VALID_COMMANDS:
                self.__mem.push(ord(c))
            elif c == _COMMENT_BEGIN:
                commend_ends_at = src.find(_COMMENT_END)
                if commend_ends_at == -1:
                    raise SyntaxError("Unclosed comment")
                src = src[:commend_ends_at]
            else:
                raise SyntaxError(f"This source contains non-Dis instruction: {c}")

        l = len(self.__mem)
        if l > _MAX_CELLS:
            raise MemoryError(f"This Dis VM accepts up to {_MAX_CELLS} items: {l} items found")

        self.__mem += [0 for _ in range(_MAX_CELLS - l)]
        assert(len(self.__mem) == _MAX_CELLS)

        # registers
        self.__a = 0
        self.__c = 0
        self.__d = 0

        # statuses
        self.__halt = False
        self.__wantinput = False
        self.__eof = False

    def run(self) -> None:
        """
        Runs the loaded program until it halts.

        By default,
        - input and output are done with standard input and standard output.
        - input and output are assumed to be sequence of bytes (octets).
        - when input is successfully done, unsigned octet is written to register A.
        - when input reaches to EOF, _MAX_CELLS-1 is written to register A.
        - output is done with A%256 unless A is _MAX_CELLS-1.
        """

        while self.step():
            pass

    def step(self) -> bool:
        """
        Called by run().

        Outputs self.__halt.
        """

        if self.__halt:
            return self.__halt

        instruction = self.__mem[self.__c]
        data = self.__mem[self.__d]

        match instruction:
            case 33:
                # ! is halt
                self.__halt = True

            case 42:
                # * is load
                self.__d = data

            case 62:
                # > is right rotate
                self.__a = self.__mem[self.__d] = rotate(data)

            case 94:
                # ^ is jump
                self.__c = data

            # case 95: _ and others are NOP

            case 123:
                # { is output OR halt
                if self.__a == _MAX_CELLS - 1:
                    self.__halt = True
                c = self.__a % 256
                sys.stdout.buffer.write(bytearray(c))

            case 124:
                # | is operation / subtract without borrow
                self.__a = self.__mem[self.__d] = subtract_without_borrow(self.__a, data)

            case 125:
                # } is input
                try:
                    self.__a: int = sys.stdin.buffer.read(1)[0]
                except IndexError:
                    self.__a = _MAX_CELLS - 1

        self.__c = ( self.__c + 1 ) % _MAX_CELLS
        self.__d = ( self.__d + 1 ) % _MAX_CELLS

        return self.__halt

def rotate(x: int):
    ...

def subtract_without_borrow(x: int, y: int):
    ...
