def start_interface(interface=None):
    """
    Start the live interface for the given interface.
    :param interface: The interface to start. If None, use the default interface.
    :return: None
    """
    if interface is None:
        return  # No interface provided, do not start anything
    else:
        if interface == "web":
            from livevars.interfaces.web.server import run_web_interface
            run_web_interface()
    