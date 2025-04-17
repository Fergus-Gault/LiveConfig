import threading
from liveconfig.core import manager

from ... import logger

def run_cli():
    """
    Run the CLI thread.
    """
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
    print("Usage: <instance_name> <attr_name> <new_value>")
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

def handle_inputs(user_input):
    if user_input.strip().lower() in {"exit", "quit"}:
        return 0
    if user_input.strip().lower() == "save":
        manager.file_handler.save()
        return 1
    if user_input.strip().lower() == "list":
        print(manager.get_all_instances())
        return 1
    # if user_input.strip().lower() == "reload":
    #     manager.file_handler.reload()
    #     return 1
    
    

def parse_input(user_input):
    """
    This function parses the input from the user.

    It checks for at least three distinct parts, instance name, attribute name, and the new value.
    It ensures that the new value is the same type as the current value, and handles errors graciously.

    """
    try:
        parts = user_input.strip().split(" ", 2)
        if len(parts) != 3:
            print("Invalid input format. Use: <instance_name> <attr_name> <new_value>")
            return

        instance_name, attr_name, value = parts

        # Set new value
        manager.set_live_instance_attr_by_name(instance_name, attr_name, value)

    except Exception as e:
        logger.error(f"ERROR: Error parsing input: {e}")