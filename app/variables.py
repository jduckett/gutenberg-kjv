from .directory import Directory

import os

tree = """
data
    json
        nt
        ot
    text
        nt
        ot
"""

dirs = Directory(os.path.abspath("."), tree)

dirs.sync_file_system()
