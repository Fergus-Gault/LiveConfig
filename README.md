# **LiveConfig** - v0.2.0-beta

LiveConfig is a Python package that allows developers to edit variables in real-time. All variables can be saved to a .json file and loaded automatically on startup. Function triggers can run a function from the interface and change behaviour during runtime. No more restarting your program every time you make a minor adjustment.

> ⚠️ This is a beta release (v0.2.0-beta). APIs and features may change in future updates.

## Features

- Class attribute editing - Edit attributes of class instances in real-time.
- Variable editing - Edit the values of variables in real-time.
- Function triggers - Trigger a function from the interface.
- File-handling - Attributes and values are saved to a file and automatically loaded on startup.
- Multiple interfaces\* - Interact with LiveConfig through the command line or a web interface.
- Easy to use - Adding an instance to LiveConfig only requires editing one line of code.

\* Interface system is under development — currently supports CLI and basic web interface. More coming soon!

## Installation

```bash
pip install liveconfig
```

## Usage

### Setup

```python
from liveconfig import LiveConfig, start_interface

# Immediately after import, setup the path to the file where variables will be saved and loaded from
LiveConfig("./path/to/file.json")

# Start the interface of choice. "web" or "cli"
start_interface("web")
```

- `LiveConfig(path)` - **MUST** be done before importing any live classes or instances, recommended to do right after importing LiveConfig.

### Live instances

```python
from liveconfig import liveclass, liveinstance

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

- `@liveclass` - Marks a class so its instances can be tracked and edited.
- `liveinstance(<name>)(<Class()>)` - Registers a specific instance for live editing, using the given name as its identifier.

### Live variables

```python
from liveconfig import livevar

var = livevar("example")("Example String")
```

- `livevar(<name>)(<value>)` - Register a variable for live editing. The name must be unique to the program.

### Function triggers

```python
from liveconfig import trigger

@trigger
def example_function():
    print("This function can be triggered from the interface")
```

- `@trigger` - A decorator for a function that can be triggered from the interface.

## Future Features

- Greater functionality for triggers.
- Support for databases.
- More interface options.
- Allow users to create their own interface.
- Ability to prevent an attribute being changed.
- Ensure minimal overhead if LiveConfig is disabled.

## About

LiveConfig is a lightweight Python package that lets you update variables at runtime—perfect for live-tuning values in long-running processes like computer vision pipelines, simulations, or game logic. No more restarting your program for every tweak. Create function triggers for use cases such as resetting, deleting, tweaking.

## License

[MIT](https://choosealicense.com/licenses/mit/)
