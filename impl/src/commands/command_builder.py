import logging

import constants


class CommandBuilder:
    """
    The CommandBuilder takes care of constructing command line commands

    It constructs the commands based on the received parameters.
    Its output is the command that is later send to the executor.

    Args:
        command_executor (CommandExecutor): command executor
        logger (Logger): logger
    """

    def __init__(self, command_executor, logger):
        self.command_executor = command_executor
        self.logger = logger
        self.output = ""

    def command(self, command_name, supplement):
        """Build and execute a command based on the command name and optional arguments.

        Args:
            command_name (str): The name of the command to build
            supplement: Optional arguments for the command

        Returns:
            reaction: A string defining how the program should react to a specific output
        """
        self.output = ""  # Resseting output
        if command_name in self.command_mappings:
            avaiability = self.check_avaiability()
            if avaiability == 'missing_reader':
                self.output = "The reader is missing."
                return avaiability
            if avaiability == 'missing_pm3':
                self.output = "The pm3 program is missing."
                return avaiability
            command = self.single_command(command_name, supplement)
            reaction = self.command_executor.execute_command(command, command_name)
            self.output = self.command_executor.get_output()
        else:
            self.logger.log(
                f"Command not found: {command_name}",
                level=logging.WARNING)

        return reaction

    def single_command(self, command_name, supplement):
        """A skeleton for a command execution

        Args:
            command_name (str): The command name
            supplement (str): An optional supplement (arguments) for the command

        Returns:
            string  containing the command to execute
        """
        return "pm3 -c \'" + self.command_mappings[command_name](self, supplement) + "\'"

    def lf_search(self, *args):
        # pylint: disable=unused-argument
        return "lf search"

    def hf_search(self, *args):
        # pylint: disable=unused-argument
        return "hf search"

    def load_em410x_id(self, *args):
        # pylint: disable=unused-argument
        return "lf em 410x reader"

    def load_mf_id(self, *args):
        # pylint: disable=unused-argument
        return "hf mf info"

    def load_legic_card(self, *args):
        # pylint: disable=unused-argument
        return "hf legic dump"

    def write_em410x_card(self, supplement):
        if supplement is None:
            self.logger.log("Fail in writing em410x - missing id", level=logging.WARNING)
        return "lf em 410x clone --id " + supplement

    def write_legic_card(self, supplement):
        if supplement is None:
            self.logger.log("Fail in writing legic - missing file", level=logging.WARNING)
        return "hf legic restore -f " + supplement

    def emulate_em410x_id(self, supplement):
        if supplement is None:
            self.logger.log("Fail in emulating EM410X - missing id", level=logging.WARNING)
        return "lf em 410x sim --id " + supplement

    def emulate_desfire_id(self, supplement):
        if supplement is None:
            self.logger.log("Fail in emulating MF Desfire - missing id", level=logging.WARNING)
        return "hf 14a sim -t 3 --uid " + supplement

    def emulate_mf_classic_1k_id(self, supplement):
        if supplement is None:
            self.logger.log("Fail in emulating MF Classic 1k - missing id", level=logging.WARNING)
        return "hf 14a sim -t 1 --uid " + supplement

    def emulate_mf_classic_4k_id(self, supplement):
        if supplement is None:
            self.logger.log("Fail in emulating MF Classic 4k - missing id", level=logging.WARNING)
        return "hf 14a sim -t 8 --uid " + supplement

    def emulate_mf_ultralight_id(self, supplement):
        if supplement is None:
            self.logger.log("Fail in emulating MF Ultralight - missing id", level=logging.WARNING)
        return "hf 14a sim -t 2 --uid " + supplement

    def emulate_legic_card(self, supplement):
        return "hf legic sim " + supplement

    def eload_legic_card(self, supplement):
        return "hf legic eload -f " + supplement

    def autopwn_mf_card(self, supplement):
        return "hf mf autopwn " + supplement

    def write_mf_card(self, supplement):
        return "hf mf restore " + supplement

    def eload_mf_card(self, supplement):
        return "hf mf eload " + supplement

    def emulate_mf_card(self, supplement):
        return "hf mf sim -i " + supplement

    def load_mf_ultralight_card(self, *args):
        # pylint: disable=unused-argument
        return "hf mfu dump"

    def write_mf_ultralight_card(self, supplement):
        return "hf mfu restore " + supplement

    def emulate_mf_ultralight_card(self, supplement):
        return "hf mfu sim " + supplement

    def eload_mf_ultralight_card(self, supplement):
        return "hf mfu eload " + supplement

    def change_mf_classic_id(self, supplement):
        return "hf mf " + supplement

    def change_mf_ultralight_id(self, supplement):
        return "hf mfu setuid -u " + supplement

    def list_ports(self):
        return "pm3 --list"

    def check_avaiability(self):
        command = self.list_ports()
        return self.command_executor.execute_command(command, "list_ports")

    # Mapping of command names to corresponding building methods
    command_mappings = {
        constants.LF_SEARCH: lf_search,
        constants.HF_SEARCH: hf_search,
        constants.LOAD_EM410X_ID: load_em410x_id,
        constants.LOAD_MF_ID: load_mf_id,
        constants.WRITE_EM410X_CARD: write_em410x_card,
        constants.EMULATE_DESFIRE_ID: emulate_desfire_id,
        constants.EMULATE_EM410X_ID: emulate_em410x_id,
        constants.EMULATE_MF_CLASSIC_1K_ID: emulate_mf_classic_1k_id,
        constants.EMULATE_MF_CLASSIC_4K_ID: emulate_mf_classic_4k_id,
        constants.EMULATE_MF_ULTRALIGHT_ID: emulate_mf_ultralight_id,
        constants.LOAD_LEGIC_CARD: load_legic_card,
        constants.WRITE_LEGIC_CARD: write_legic_card,
        constants.ELOAD_LEGIC_CARD: eload_legic_card,
        constants.EMULATE_LEGIC_CARD: emulate_legic_card,
        constants.AUTOPWN_MF_CARD: autopwn_mf_card,
        constants.WRITE_MF_CARD: write_mf_card,
        constants.ELOAD_MF_CARD: eload_mf_card,
        constants.EMULATE_MF_CARD: emulate_mf_card,
        constants.LOAD_MF_ULTRALIGHT_CARD: load_mf_ultralight_card,
        constants.WRITE_MF_ULTRALIGHT_CARD: write_mf_ultralight_card,
        constants.EMULATE_MF_ULTRALIGHT_CARD: emulate_mf_ultralight_card,
        constants.ELOAD_MF_ULTRALIGHT_CARD: eload_mf_ultralight_card,
        constants.CHANGE_MF_CLASSIC_ID: change_mf_classic_id,
        constants.CHANGE_MF_ULTRALIGHT_ID: change_mf_ultralight_id,
        # Add more mappings for other commands...
    }

    def get_output(self):
        return self.output
