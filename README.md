# **LiveConfig** - v0.1.2-beta

LiveConfig is a Python package that allows developers to edit variables in real-time. All variables can be saved to a .json file and loaded automatically on startup. No more restarting your program every time you make a minor adjustment.

> ⚠️ This is a beta release (v0.1.2-beta). APIs and features may change in future updates.

## Features

- Class attribute editing - Edit attributes of class instances in real-time.
- File-handling - Attributes and values are saved to a file and automatically loaded on startup.
- Multiple interfaces\* - Interact with LiveConfig through the command line or a web interface.
- Easy to use - Adding an instance to LiveConfig only requires editing one line of code.

\* Interface system is under development — currently supports CLI and basic web interface. More coming soon!

## Installation

```bash
pip install liveconfig
```

## Usage

```python
from liveconfig import LiveConfig, liveclass, liveinstance, start_interface
# Initialize LiveConfig with the path to your JSON save file, do this before any other imports
LiveConfig("./files/variables.json")

# Start the user interface — use "cli" or "web" (more coming soon)
start_interface("web", port=5000)

# Decorate your class to make it live-editable
@liveclass
class Config:
    def __init__(self):
        self.text = "Hello, World"
        self.width = 640
        self.height = 480

# Register an instance of the class for editing
config = liveinstance("config")(Config())

```

- `LiveConfig(path)` - **MUST** be done before importing any live classes or instances, recommended to do right after importing LiveConfig
- `@liveclass` - Marks a class so its instances can be tracked and edited.
- `liveinstance(name)` - Registers a specific instance for live editing, using the given name as its identifier.

## Future Features

- Support for functions and individual variables
- Support for databases
- More interface options
- Allow users to create their own interface
- Ability to prevent an attribute being changed.
- Ensure minimal overhead if LiveConfig is disabled.
- Function triggers, runs a function once.

## About

LiveConfig is a lightweight Python package that lets you update variables at runtime—perfect for live-tuning values in long-running processes like computer vision pipelines, simulations, or game logic. No more restarting your program for every tweak.

## License

[MIT](https://choosealicense.com/licenses/mit/)
