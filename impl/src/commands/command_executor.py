import logging
import subprocess


class CommandExecutor:
    """
    A class that takes care of executing the given command in a subprocess and determines signals that are telling
    how to react to a specific output

    Args:
        output_handler (OutputHandler): A class that is processing the output, parsing text
        logger (Logger): The logger
    """

    def __init__(self, output_handler, logger):
        self.output_handler = output_handler
        self.logger = logger
        self.output = ""

    def execute_command(self, command, command_name):
        """Execute a command in a subprocess.

        Args:
            command (str): The command to execute
            command_name (str): A string defining the command type

        Returns:
            A string defining the reaction to the command
        """
        to_perform = 'nothing'
        self.output = ""
        try:
            self.logger.log(
                f"Executing command '{command}'.",
                level=logging.INFO)
            process = subprocess.run(command, shell=True, capture_output=True, text=True)
            to_perform = self.output_handler.handle_output(process.stdout + process.stderr, command_name)
        except subprocess.TimeoutExpired:
            self.logger.log(
                f"Command '{command}' timed out.",
                level=logging.WARNING)
        except Exception as e:
            self.logger.log(f"An error occurred: {e}", level=logging.WARNING)

        return self.command_mappings[to_perform](self)

    def output_handled(self):
        self.output = self.output_handler.get_output()
        return "output_handled"

    def missing_reader(self):
        return "missing_reader"

    def missing_pm3(self):
        return "missing_pm3"

    def no_card_found(self):
        return "No card found"

    def problem(self):
        return "problem"

    def nothing(self):
        return "nothing"

    def unknown_output(self):
        return "unknown_output"

    # Mapping of command names to corresponding building methods
    command_mappings = {
        "missing_reader": missing_reader,
        "missing_pm3": missing_pm3,
        "output_handled": output_handled,
        "no_card_found": no_card_found,
        "nothing": nothing,
        "unknown_output": unknown_output,
        "problem": problem
        # Add more mappings for other commands...
    }

    def get_output(self):
        return self.output
