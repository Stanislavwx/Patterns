import os, sys
# Додати корінь проєкту у sys.path, щоб 'from minidb import *' працювало для pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
