#!/usr/bin/env python3

# This script is the main entry point for the gemmit tool.
# It dispatches the command-line arguments to the appropriate command module.

import sys
from commands import generate

def main():
    # Pass all arguments except the script name to the generate command.
    generate.run(sys.argv[1:])

if __name__ == '__main__':
    main()
