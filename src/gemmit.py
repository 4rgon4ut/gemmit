
#!/usr/bin/env python3

import sys
from commands import generate

def main():
    """Main function."""
    # The first argument is the template name, which is passed to the generate command.
    generate.run(sys.argv[1:])

if __name__ == '__main__':
    main()
