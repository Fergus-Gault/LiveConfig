def start_interface(interface: str = None, **kwargs) -> None:
    """
    This method starts the interface based on the provided type.
    It can be a web interface or a command-line interface (CLI).

    Args:
        interface (str, optional): The interface type. Defaults to None.

    Raises:
        ValueError: Raised if the interface type is invalid.
    """
    if interface is None: return

    else:
        if interface == "web":
            port = parse_port(port=kwargs.get("port", 5000))
            from liveconfig.interfaces.web.server import run_web_interface
            run_web_interface(port)

        elif interface == "cli":
            from liveconfig.interfaces.cli.cli import run_cli
            run_cli()

        else:
            raise ValueError("Invalid interface type.")
    
def parse_port(port: int) -> int:
    """Parse and validate the port number."""

    if not isinstance(port, int):
        raise ValueError("Port must be an integer.")
    
    if port < 1024 or port > 65535:
        raise ValueError("Port number must be between 1024 and 65535.")
    
    return port