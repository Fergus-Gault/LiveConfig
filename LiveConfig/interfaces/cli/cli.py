import threading
from liveconfig.core import manager


def run_cli():
    """Run the CLI thread."""
    threading.Thread(target=run_cli_thread, daemon=True).start()


def run_cli_thread():
    """
    This function starts the CLI, listening for input and prompting the user of the correct usage.

    It attempts to use the prompt_toolkit for a better experience (on windows).
    This is useful if there are a lot of messages being printed to console.

    If user is using an unsupported CLI then it fallsback to the default input behaviour.
    """
    try:
        from prompt_toolkit import PromptSession
        from prompt_toolkit.patch_stdout import patch_stdout
        session = PromptSession(">>> ")
        use_prompt_toolkit = True
    except Exception as e:
        use_prompt_toolkit = False
    print(
        "Usage: \n"
        "Format to edit an instance: <i/instance> <instance_name> <attr_name> <value>\n"
        "Format to edit a variable: <v/variable> <variable_name> <value>\n"
        "Format to trigger a function: <t/trigger> <function_name> *<arg1_name=value> *<arg2_name=value> ...\n"
        "Commands: quit, save, reload, list\n"
    )
    if use_prompt_toolkit:
        with patch_stdout():
            while True:
                try:
                    user_input = session.prompt()
                    response = handle_inputs(user_input)
                    if response == 0:
                        break
                    elif response == 1:
                        continue
                    else:
                        parse_input(user_input)
                except (EOFError, KeyboardInterrupt):
                    break
    else:
        while True:
            try:
                user_input = input(">>> ")
                response = handle_inputs(user_input)
                if response == 0:
                    break
                elif response == 1:
                    continue
                else:
                    parse_input(user_input)
            except KeyboardInterrupt:
                break

def handle_inputs(user_input: str):
    """
    This function handles the inputs from the user.
    It runs the appropriate function based on the input.

    Args:
        user_input (str): Input from the user.

    Returns:
        Literal: Returns 0 if the user wants to exit, 
        1 if the user wants to save, 
        and None otherwise.
    """
    parts = user_input.strip().split(" ")
    if user_input.strip().lower() in {"exit", "quit", "ex", "q"}:
        return 0
    if user_input.strip().lower() == "save":
        manager.file_handler.save()
        return 1
    if parts[0].strip().lower() == "list":
        if len(parts) == 2:
            if parts[1].strip().lower() in {"instances", "instance", "i"}:
                print(manager.list_all_instances())
            elif parts[1].strip().lower() in {"variables", "variable", "v"}:
                print(manager.list_all_variables())
            elif parts[1].strip().lower() in {"triggers", "trigger", "t"}:
                print(manager.list_all_triggers())
            else:
                print("Please specify 'instances', 'variables', or 'triggers' to list. e.g 'list instances'")
        elif len(parts) == 3:
            if parts[1].strip().lower() in {"instances", "instance", "i"}:
                print(manager.list_instance_attrs_by_name(parts[2]))
            elif parts[1].strip().lower() in {"variables", "variable", "v"}:
                print(manager.list_variable_by_name(parts[2]))
            elif parts[1].strip().lower() in {"triggers", "trigger", "t"}:
                print(manager.list_all_trigger_args(parts[2]))
            else:
                print("Please specify 'instances' or 'variables' to list. e.g 'list instances <name>'")
        else:
            print("Please specify 'instances' or 'variables' to list. e.g 'list instances <name>'")
        return 1
    if user_input.strip().lower() == "reload":
        manager.file_handler.reload()
        return 1
    
    

def parse_input(user_input: str) -> None:
    """
    This function parses the user input 
    and calls the appropriate function to set the value.

    Args:
        user_input (str): Input from the user.
    """
    try:
        method = user_input[0].lower()
        if method not in ("i", "instance", "v", "variable", "t", "trigger"):
            print("Invalid method. Use 'i' or 'v' for instance or variable.")
            return
        
        if method in ("i", "instance"):
            parts = user_input.strip().split(" ", 3)
            if len(parts) != 4:
                print("Invalid input format. Use: <instance_name> <attr_name> <new_value>")
                return

            _, instance_name, attr_name, value = parts

            # Set new value
            manager.set_live_instance_attr_by_name(instance_name, attr_name, value)
        
        elif method in ("v", "variable"):
            parts = user_input.strip().split(" ", 2)
            if len(parts) != 3:
                print("Invalid input format. Use: <variable_name> <new_value>")
                return

            _, variable_name, value = parts

            # Set new value
            manager.set_live_variable_by_name(variable_name, value)

        elif method in ("t", "trigger"):
            parts = user_input.strip().split(" ", 1)
            if len(parts) < 2:
                print("Invalid input format. Use: <function_name> <*arg1> <*arg2> ...")
                return

            _, function_name_and_args = parts
            function_parts = function_name_and_args.split(" ", 1)
            function_name = function_parts[0].strip()
            args = function_parts[1].split(" ") if len(function_parts) > 1 else []

            # Convert args to a dictionary of keyword arguments
            kwargs = {}
            for arg in args:
                if "=" in arg:
                    key, value = arg.split("=", 1)
                    kwargs[key.strip()] = value.strip()
                else:
                    print(f"Invalid argument format: {arg}. Use key=value format.")
                    return

            manager.trigger_function_by_name(function_name, **kwargs)

    except Exception as e:
        pass