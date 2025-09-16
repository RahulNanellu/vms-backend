import inspect
import app.main as m

print("main.py loaded from:", inspect.getfile(m))

print("\nRegistered routes:")
for r in m.app.routes:
    print(" -", getattr(r, "path", None), getattr(r, "methods", None))
