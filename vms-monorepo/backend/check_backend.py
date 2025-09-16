import os, sys, inspect
BACKEND = os.path.abspath(os.path.dirname(__file__))
if BACKEND not in sys.path: sys.path.insert(0, BACKEND)
import app.main as m
p = os.path.abspath(inspect.getfile(m))
print("Active app.main:", p)
print("Backend root   :", os.path.dirname(os.path.dirname(p)))
