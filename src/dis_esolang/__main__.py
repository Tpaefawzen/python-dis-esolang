"""
Interpreter as a command
"""

from dis_esolang import Dis

def main(argv):
    with open(argv[1], "r") as f:
        s = f.read()

    Dis(s).run()

if __name__ == "__main__":
    import sys
    main(sys.argv)
