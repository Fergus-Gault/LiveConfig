import threading
from liveconfig.core import manager

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
                    if user_input.strip().lower() in {"exit", "quit"}:
                        break
                    if user_input.strip().lower() == "save":
                        manager.file_handler.save()
                        continue
                    parse_input(user_input)
                except (EOFError, KeyboardInterrupt):
                    break
    else:
        while True:
            try:
                user_input = input(">>> ")
                if user_input.strip().lower() in {"exit", "quit"}:
                    break
                if user_input.strip().lower() == "save":
                        manager.file_handler.save()
                        continue
                parse_input(user_input)
            except KeyboardInterrupt:
                break
    
    


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
        instance = manager.get_live_instance_by_name(instance_name)

        if instance is None:
            print(f"No instance found with name '{instance_name}'")
            return

        # Get current type of the attribute
        current_attr_value = getattr(instance, attr_name, None)
        if current_attr_value is None:
            print(f"'{attr_name}' does not exist on '{instance_name}'")
            return

        attr_type = type(current_attr_value)
        try:
            new_value = attr_type(value)  # Try to cast to the same type
            # Set new value
            setattr(instance, attr_name, new_value)
            print(f"Set {instance_name}.{attr_name} = {new_value}")
        except Exception as e:
            print(f"Types do not match. Must by type {attr_type}")


    except Exception as e:
        print(f"Error parsing input: {e}")