import logging
import os
import shutil
from datetime import datetime

import constants


class FileHandler:
    """
    The FileHandler handles everything associated with the filesystem

    It creates files, moves them or edit them.

    Args:
        logger (Logger): The logger
    """

    def __init__(self, logger):
        self.logger = logger
        # Expand tilde to full path
        self.root_folder = os.path.expanduser(constants.ROOT_FOLDER)

    def save_id(self, new_id, card_type):
        """Saves the id of the specific card to a specific folder"""

        current_datetime = datetime.now().strftime(constants.DATETIME_FORMAT)
        self.create_dir_if_not_exist(os.path.join(self.root_folder, constants.IDS))
        if card_type == constants.EM410X:
            path_to_folder = os.path.join(self.root_folder, constants.IDS, constants.EM410X)
            self.create_dir_if_not_exist(path_to_folder)
            self.write_to_file(os.path.join(path_to_folder, new_id) + constants.TXT, current_datetime)
        elif card_type == constants.MF_DESFIRE:
            path_to_folder = os.path.join(self.root_folder, constants.IDS, constants.MF_DESFIRE)
            self.create_dir_if_not_exist(path_to_folder)
            self.write_to_file(os.path.join(path_to_folder, new_id) + constants.TXT, current_datetime)
        elif card_type == constants.MF_CLASSIC_1K:
            path_to_folder = os.path.join(self.root_folder, constants.IDS, constants.MF_CLASSIC_1K)
            self.create_dir_if_not_exist(path_to_folder)
            self.write_to_file(os.path.join(path_to_folder, new_id) + constants.TXT, current_datetime)
        elif card_type == constants.MF_CLASSIC_4K:
            path_to_folder = os.path.join(self.root_folder, constants.IDS, constants.MF_CLASSIC_4K)
            self.create_dir_if_not_exist(path_to_folder)
            self.write_to_file(os.path.join(path_to_folder, new_id) + constants.TXT, current_datetime)
        elif card_type == constants.MF_ULTRALIGHT:
            path_to_folder = os.path.join(self.root_folder, constants.IDS, constants.MF_ULTRALIGHT)
            self.create_dir_if_not_exist(path_to_folder)
            self.write_to_file(os.path.join(path_to_folder, new_id) + constants.TXT, current_datetime)

    def write_to_file(self, file_path, content):
        """Writes to a specific file given content"""

        with open(file_path, 'w', encoding='ascii') as file:
            file.write(content)
            print(f"Content written to '{file_path}'")

    def create_dir_if_not_exist(self, name):
        """Creates a dir in a given path if it does not exist"""
        # Check if the directory exists
        if not os.path.exists(name):
            # If it doesn't exist, create it
            os.makedirs(name)
            self.logger.log(f"'{name}' directory created successfully.", level=logging.INFO)

    def get_card_ids_and_dates(self, card_type):
        """Gets all saved IDs of a specific card type and returns it as a list"""
        if not os.path.exists(self.root_folder):
            self.logger.log("The root folder does not exist.", level=logging.CRITICAL)
            return []
        folder_path = os.path.join(self.root_folder, constants.IDS)
        if not os.path.exists(folder_path):
            self.logger.log(f"The {constants.IDS} folder does not exist.", level=logging.INFO)
            return []
        if card_type == constants.EM410X:
            folder_path = os.path.join(folder_path, constants.EM410X)
        if card_type == constants.MF_CLASSIC_1K:
            folder_path = os.path.join(folder_path, constants.MF_CLASSIC_1K)
        if card_type == constants.MF_CLASSIC_4K:
            folder_path = os.path.join(folder_path, constants.MF_CLASSIC_4K)
        if card_type == constants.MF_ULTRALIGHT:
            folder_path = os.path.join(folder_path, constants.MF_ULTRALIGHT)
        if card_type == constants.MF_DESFIRE:
            folder_path = os.path.join(folder_path, constants.MF_DESFIRE)
        if not os.path.exists(folder_path):
            self.logger.log(f"The {constants.EM410X} folder does not exist.", level=logging.INFO)
            return []

        cards = []

        for filename in os.listdir(folder_path):
            if filename.endswith('.txt'):
                file_path = os.path.join(folder_path, filename)
                with open(file_path, 'r', encoding='ascii') as file:
                    datetime_str = file.readline().strip()  # Read the first line and strip newline characters
                    id_ = filename.split('.')[0]  # Extract ID from filename
                    cards.append((id_, datetime_str))

        return cards

    def move_dump_file(self, dump_file, card_type):
        """Moves freshly created dumpfile of a specific card type to a specific subdir"""

        if not os.path.exists(self.root_folder):
            self.logger.log("The root folder does not exist.", level=logging.CRITICAL)
            return
        self.create_dir_if_not_exist(os.path.join(self.root_folder, constants.DUMPS))

        if card_type == constants.LEGIC_PRIME:
            path_to_folder = os.path.join(self.root_folder, constants.DUMPS, constants.LEGIC_PRIME)
            self.create_dir_if_not_exist(path_to_folder)
        elif card_type == constants.MF_CLASSIC_1K:
            path_to_folder = os.path.join(self.root_folder, constants.DUMPS, constants.MF_CLASSIC_1K)
            self.create_dir_if_not_exist(path_to_folder)
        elif card_type == constants.MF_CLASSIC_2K:
            path_to_folder = os.path.join(self.root_folder, constants.DUMPS, constants.MF_CLASSIC_2K)
            self.create_dir_if_not_exist(path_to_folder)
        elif card_type == constants.MF_CLASSIC_4K:
            path_to_folder = os.path.join(self.root_folder, constants.DUMPS, constants.MF_CLASSIC_4K)
            self.create_dir_if_not_exist(path_to_folder)
        elif card_type == constants.MF_CLASSIC_MINI:
            path_to_folder = os.path.join(self.root_folder, constants.DUMPS, constants.MF_CLASSIC_MINI)
            self.create_dir_if_not_exist(path_to_folder)
        elif card_type == constants.MF_ULTRALIGHT:
            path_to_folder = os.path.join(self.root_folder, constants.DUMPS, constants.MF_ULTRALIGHT)
            self.create_dir_if_not_exist(path_to_folder)
        else:
            self.logger.log(f"Unknown card type: {card_type}", level=logging.WARNING)

        path_to_file = os.path.join(self.root_folder, dump_file)

        # If the file exists, remove it, to update it
        if os.path.exists(os.path.join(path_to_folder, dump_file)):
            os.remove(os.path.join(path_to_folder, dump_file))

        # Move the file to the specified folder
        shutil.move(path_to_file, path_to_folder)

        # Remove the generated json file
        dump_file_json = dump_file[:-4] + '.json'
        if os.path.exists(os.path.join(self.root_folder, dump_file_json)):
            os.remove(os.path.join(self.root_folder, dump_file_json))

    def move_keys_file(self, keys_file, card_type):
        """Moves freshly created keys file of a specific card type to a specific subdir"""

        if not os.path.exists(self.root_folder):
            self.logger.log("The root folder does not exist.", level=logging.CRITICAL)
            return
        self.create_dir_if_not_exist(os.path.join(self.root_folder, constants.KEYS))

        if card_type == constants.LEGIC_PRIME:
            path_to_folder = os.path.join(self.root_folder, constants.KEYS, constants.LEGIC_PRIME)
            self.create_dir_if_not_exist(path_to_folder)
        elif card_type == constants.MF_CLASSIC_1K:
            path_to_folder = os.path.join(self.root_folder, constants.KEYS, constants.MF_CLASSIC_1K)
            self.create_dir_if_not_exist(path_to_folder)
        elif card_type == constants.MF_CLASSIC_2K:
            path_to_folder = os.path.join(self.root_folder, constants.KEYS, constants.MF_CLASSIC_2K)
            self.create_dir_if_not_exist(path_to_folder)
        elif card_type == constants.MF_CLASSIC_4K:
            path_to_folder = os.path.join(self.root_folder, constants.KEYS, constants.MF_CLASSIC_4K)
            self.create_dir_if_not_exist(path_to_folder)
        elif card_type == constants.MF_CLASSIC_MINI:
            path_to_folder = os.path.join(self.root_folder, constants.KEYS, constants.MF_CLASSIC_MINI)
            self.create_dir_if_not_exist(path_to_folder)
        else:
            self.logger.log(f"Unknown card type: {card_type}", level=logging.WARNING)

        path_to_file = os.path.join(self.root_folder, keys_file)

        # If the file exists, remove it, to update it
        if os.path.exists(os.path.join(path_to_folder, keys_file)):
            os.remove(os.path.join(path_to_folder, keys_file))

        # Move the file to the specified folder
        shutil.move(path_to_file, path_to_folder)

    def get_card_dumps(self, card_type):
        """Lists all card dumps of a specific type"""

        if not os.path.exists(self.root_folder):
            self.logger.log("The root folder does not exist.", level=logging.CRITICAL)
            return []
        folder_path = os.path.join(self.root_folder, constants.DUMPS)
        if not os.path.exists(folder_path):
            self.logger.log(f"The {constants.DUMPS} folder does not exist.", level=logging.INFO)
            return []

        if card_type == constants.LEGIC_PRIME:
            folder_path = os.path.join(folder_path, constants.LEGIC_PRIME)
        elif card_type == constants.MF_CLASSIC_1K:
            folder_path = os.path.join(folder_path, constants.MF_CLASSIC_1K)
        elif card_type == constants.MF_CLASSIC_2K:
            folder_path = os.path.join(folder_path, constants.MF_CLASSIC_2K)
        elif card_type == constants.MF_CLASSIC_4K:
            folder_path = os.path.join(folder_path, constants.MF_CLASSIC_4K)
        elif card_type == constants.MF_CLASSIC_MINI:
            folder_path = os.path.join(folder_path, constants.MF_CLASSIC_MINI)
        elif card_type == constants.MF_ULTRALIGHT:
            folder_path = os.path.join(folder_path, constants.MF_ULTRALIGHT)
        else:
            self.logger.log(f"Unknown card type: {card_type}", level=logging.WARNING)

        if not os.path.exists(folder_path):
            self.logger.log(f"The {card_type} folder does not exist.", level=logging.INFO)
            return []

        dump_files = []

        for filename in os.listdir(folder_path):
            if filename.endswith('.bin'):
                dump_files.append(filename)

        return dump_files

    def get_card_keys(self, card_type):
        """Lists all card keys of a specific type"""

        if not os.path.exists(self.root_folder):
            self.logger.log("The root folder does not exist.", level=logging.CRITICAL)
            return []
        folder_path = os.path.join(self.root_folder, constants.KEYS)
        if not os.path.exists(folder_path):
            self.logger.log(f"The {constants.KEYS} folder does not exist.", level=logging.INFO)
            return []

        if card_type == constants.LEGIC_PRIME:
            folder_path = os.path.join(folder_path, constants.LEGIC_PRIME)
        elif card_type == constants.MF_CLASSIC_1K:
            folder_path = os.path.join(folder_path, constants.MF_CLASSIC_1K)
        elif card_type == constants.MF_CLASSIC_2K:
            folder_path = os.path.join(folder_path, constants.MF_CLASSIC_2K)
        elif card_type == constants.MF_CLASSIC_4K:
            folder_path = os.path.join(folder_path, constants.MF_CLASSIC_4K)
        elif card_type == constants.MF_CLASSIC_MINI:
            folder_path = os.path.join(folder_path, constants.MF_CLASSIC_MINI)
        else:
            self.logger.log(f"Unknown card type: {card_type}", level=logging.WARNING)

        if not os.path.exists(folder_path):
            self.logger.log(f"The {card_type} folder does not exist.", level=logging.INFO)
            return []

        keys_files = []

        for filename in os.listdir(folder_path):
            if filename.endswith('.bin'):
                keys_files.append(filename)

        return keys_files
