from . import logger


def start_interface(interface=None, **kwargs):
    """
    Start the live interface for the given interface.
    'web' - Locally hosted web interface.
    'cli' - CLI with typed commands.

    User can optionally specify a port to use for the web interface.
    """
    if interface is None:
        return  # No interface provided, do not start anything
    else:
        if interface == "web":
            port = 5000
            for name, value in kwargs.items():
                if name == "port":
                    try:
                        port = int(value)
                    except Exception as e:
                        logger.warning(f"WARNING: Failed to set port to {value}, using port 5000: {e}")
                    break
            from liveconfig.interfaces.web.server import run_web_interface
            run_web_interface(port)

        elif interface == "cli":
            from liveconfig.interfaces.cli.cli import run_cli
            run_cli()
        else:
            
            raise ValueError("Invalid interface type.")
    