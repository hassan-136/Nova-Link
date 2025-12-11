import sys
import os
import tkinter
import runpy

# Add project root to Python path (optional, safe)
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Monkey-patch Tk.state to ignore 'zoomed' on Linux
original_state = tkinter.Tk.state
def patched_state(self, arg=None):
    if arg == "zoomed":
        return  # Ignore zoomed
    return original_state(self, arg)
tkinter.Tk.state = patched_state

# Run main.py as a script
main_path = os.path.join(project_root, "main.py")
runpy.run_path(main_path, run_name="__main__")
