import sys
from .hclock import zeit_ascii_string
from .clcurses import CR

if len(sys.argv) > 1:
    if sys.argv[1] == "-t":
        print(zeit_ascii_string())
        sys.exit(0)

CR.run()
