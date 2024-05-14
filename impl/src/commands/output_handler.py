import logging
import os

import constants


class OutputHandler:
    """
    The OutputHandler is a class that is parsing the text output of the command and processing it

    It for example scrapes the important info or determines if the command was successful

    Args:
         logger (Logger): The logger
    """

    def __init__(self, logger):
        self.logger = logger
        self.output = ""
        self.command_name = ""

    def handle_output(self, output, command_name):
        """Handle the output of a command

        Args:
            output (str): The output string to handle
            command_name (str): A unique command name (type)

        Returns:
            Return code name of an action that should be done next
        """
        self.output = output
        self.command_name = command_name
        self.logger.log(
            f"Output for {command_name} received: {self.output}",
            level=logging.INFO)

        command_actions = {
            'list_ports': self.handle_list_ports,
            constants.LF_SEARCH: self.handle_search,
            constants.HF_SEARCH: self.handle_search,
            constants.LOAD_EM410X_ID: self.handle_load_em410x_id,
            constants.LOAD_MF_ID: self.handle_load_mf_id,
            constants.LOAD_LEGIC_CARD: self.handle_load_legic_card,
            constants.WRITE_EM410X_CARD: self.handle_write_em410x_card,
            constants.WRITE_LEGIC_CARD: self.handle_write_legic_card,
            constants.EMULATE_EM410X_ID: self.handle_emulate_em410x_id,
            constants.EMULATE_DESFIRE_ID: self.handle_emulate_id,
            constants.EMULATE_MF_CLASSIC_1K_ID: self.handle_emulate_id,
            constants.EMULATE_MF_CLASSIC_4K_ID: self.handle_emulate_id,
            constants.EMULATE_MF_ULTRALIGHT_ID: self.handle_emulate_id,
            constants.ELOAD_LEGIC_CARD: self.handle_eload_legic_card,
            constants.EMULATE_LEGIC_CARD: self.handle_emulate_legic_card,
            constants.AUTOPWN_MF_CARD: self.handle_autopwn_mf_card,
            constants.WRITE_MF_CARD: self.handle_write_mf_card,
            constants.EMULATE_MF_CARD: self.handle_emulate_mf_card,
            constants.ELOAD_MF_CARD: self.handle_eload_mf_card,
            constants.LOAD_MF_ULTRALIGHT_CARD: self.handle_load_mf_ultralight_card,
            constants.WRITE_MF_ULTRALIGHT_CARD: self.handle_write_mf_ultralight_card,
            constants.EMULATE_MF_ULTRALIGHT_CARD: self.handle_emulate_mf_ultralight_card,
            constants.ELOAD_MF_ULTRALIGHT_CARD: self.handle_eload_mf_ultralight_card,
            constants.CHANGE_MF_CLASSIC_ID: self.handle_change_mf_classic_id,
            constants.CHANGE_MF_ULTRALIGHT_ID: self.handle_change_mf_ultralight_id
        }

        action = command_actions.get(command_name)
        if action:
            return action()

        return constants.UNKNOWN_OUTPUT

    def get_output(self):
        return self.output

    # Section of methods defining output handling for a specific command
    def handle_list_ports(self):
        if self.contains_sentence("command not found") or self.contains_sentence("'pm3' is not recognized"):
            return constants.MISSING_PM3
        if self.contains_sentence("No port found"):
            return constants.MISSING_READER
        return constants.NOTHING.value

    def handle_search(self):
        if self.command_name == constants.LF_SEARCH and (self.contains_sentence(
                "No known 125/134 kHz tags found!") or self.contains_sentence("No data found")):
            return constants.NO_CARD_FOUND
        if self.command_name == constants.HF_SEARCH and self.contains_sentence("No known/supported 13.56 MHz"):
            return constants.NO_CARD_FOUND
        self.erase_first_n_lines()
        self.remove_lines_with_substrings()
        return constants.OUTPUT_HANDLED

    def handle_load_em410x_id(self):
        if not self.contains_sentence("EM 410x ID"):
            return constants.NO_CARD_FOUND
        self.output = self.extract_id_from_em410x()
        return constants.OUTPUT_HANDLED

    def handle_load_mf_id(self):
        loaded_id = self.extract_id_from_mf()
        if loaded_id is None:
            return constants.NO_CARD_FOUND
        self.output = loaded_id
        return constants.OUTPUT_HANDLED

    def handle_load_legic_card(self):
        saved_dump = self.extract_filename_from_backticks("bytes to binary file")
        if saved_dump is None:
            return constants.NO_CARD_FOUND
        self.output = saved_dump
        return constants.OUTPUT_HANDLED

    def handle_write_em410x_card(self):
        if not self.contains_sentence("Done"):
            return constants.NO_CARD_FOUND
        return constants.OUTPUT_HANDLED

    def handle_write_legic_card(self):
        if not self.contains_sentence("Done!"):
            return constants.NO_CARD_FOUND
        return constants.OUTPUT_HANDLED

    def handle_emulate_em410x_id(self):
        if self.contains_sentence("EM ID must include 5 hex bytes"):
            return constants.UNKNOWN_OUTPUT
        return constants.OUTPUT_HANDLED

    def handle_emulate_id(self):
        if self.contains_sentence("Please specify a 4, 7, or 10 byte UID"):
            return constants.UNKNOWN_OUTPUT
        return constants.OUTPUT_HANDLED

    def handle_eload_legic_card(self):
        if not self.contains_sentence("Done!"):
            return constants.UNKNOWN_OUTPUT
        return constants.OUTPUT_HANDLED

    def handle_emulate_legic_card(self):
        if not self.contains_sentence("Done!"):
            return constants.UNKNOWN_OUTPUT
        return constants.OUTPUT_HANDLED

    def handle_autopwn_mf_card(self):
        dump_file = self.extract_filename_from_backticks("bytes to binary file")
        keys_file = self.extract_filename_from_backticks("Found keys have been")
        if self.contains_sentence("No tag detected"):
            return constants.NO_CARD_FOUND
        if dump_file is None or keys_file is None:
            return constants.PROBLEM
        self.output = (keys_file, dump_file)
        return constants.OUTPUT_HANDLED

    def handle_write_mf_card(self):
        if not self.contains_sentence("Done!"):
            return constants.UNKNOWN_OUTPUT
        return constants.OUTPUT_HANDLED

    def handle_emulate_mf_card(self):
        if not self.contains_sentence("Enforcing"):
            return constants.UNKNOWN_OUTPUT
        return constants.OUTPUT_HANDLED

    def handle_eload_mf_card(self):
        if not self.contains_sentence("Done!"):
            return constants.UNKNOWN_OUTPUT
        return constants.OUTPUT_HANDLED

    def handle_load_mf_ultralight_card(self):
        saved_dump = self.extract_filename_from_backticks("bytes to binary file")
        if saved_dump is None:
            return constants.NO_CARD_FOUND
        self.output = saved_dump
        return constants.OUTPUT_HANDLED

    def handle_write_mf_ultralight_card(self):
        if self.contains_sentence("Can't select card"):
            return constants.PROBLEM
        return constants.OUTPUT_HANDLED

    def handle_emulate_mf_ultralight_card(self):
        if not self.contains_sentence("Done!"):
            return constants.PROBLEM
        return constants.OUTPUT_HANDLED

    def handle_eload_mf_ultralight_card(self):
        if self.contains_sentence("Error"):
            return constants.PROBLEM
        return constants.OUTPUT_HANDLED

    def handle_change_mf_classic_id(self):
        if self.contains_sentence("error") or self.contains_sentence("Can't set UID"):
            return constants.PROBLEM
        return constants.OUTPUT_HANDLED

    def handle_change_mf_ultralight_id(self):
        if self.contains_sentence("Can't select card") or self.contains_sentence("failed") or self.contains_sentence("Error"):
            return constants.PROBLEM
        return constants.OUTPUT_HANDLED

    # --------------------------------------------------------------------------------

    # Help funtions for parsing output
    def extract_id_from_em410x(self):
        # Split the input string by lines
        lines = self.output.split('\n')

        # Iterate through each line
        for line in lines:
            # Check if the line contains the substring
            if "EM 410x ID" in line:
                # Return the last 10 characters of the line
                result = line[-10:]
                return result

        # Return None if the substring is not found
        return None

    def extract_id_from_mf(self):
        # Split the input string by lines
        lines = self.output.split('\n')

        # Iterate through each line
        for line in lines:
            # Check if the line contains the substring
            if "[+]  UID:" in line:
                # Return the ID
                result = line.split(':')[-1]
                # Remove whitespace characters from the extracted string
                result = result.strip()
                # Remove any remaining spaces
                result = result.replace(' ', '')
                return result

        # Return None if substring is not found
        return None

    def extract_filename_from_backticks(self, sentence_in_line):
        # Split the input string by lines
        lines = self.output.split('\n')

        # Initialize the result string
        result = None

        for line in lines:
            if sentence_in_line in line:
                # Find the substring enclosed within backticks
                start_index = line.find('`')
                end_index = line.find('`', start_index + 1)
                if start_index != -1 and end_index != -1:
                    result = line[start_index + 1:end_index]
                break

        try:
            result = os.path.basename(result)
        except Exception:
            self.logger.log("An exception has occured while finding the dumpfile", level=logging.WARNING)
            return None

        return result

    def contains_sentence(self, sentence):
        lines = self.output.split('\n')

        # Check each line for the sentence
        for line in lines:
            if sentence in line:
                return True

        # If the sentence is not found in any line
        return False

    def erase_first_n_lines(self, n=9):
        lines = self.output.split('\n')
        self.output = '\n'.join(lines[n:])

    def remove_lines_with_substrings(self):
        substrings = ["Hint:", "QStandardPaths:", "[/]", "[\\]", "Searching for"]
        lines = self.output.split('\n')
        new_lines = [line for line in lines if not any(substring in line for substring in substrings)]
        self.output = '\n'.join(new_lines)
