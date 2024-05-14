# Constants of the program

# Folders
ROOT_FOLDER = '~/.cloner'   # A root folder of the program, has to be the same for which you ran the install.sh script
IDS = 'ids'
DUMPS = 'dumps'
KEYS = 'keys'

# Files
LOG_FILE = 'app.log'
CONFIG_FILE = 'config.txt'

# Card types
EM410X = 'em410x'
MF_CLASSIC_1K = 'mf_classic_1k'
MF_CLASSIC_2K = 'mf_classic_2k'
MF_CLASSIC_4K = 'mf_classic_4k'
MF_ULTRALIGHT = 'mf_ultralight'
MF_CLASSIC_MINI = 'mf_classic_mini'
MF_DESFIRE = 'mf_desfire'
LEGIC_PRIME = 'legic_prime'

# File types
TXT = '.txt'

# Formats
DATETIME_FORMAT = "%d. %m. %Y %H:%M"

# Command names
LOAD_MF_ID = 'load_mf_id'
LOAD_EM410X_ID = 'load_em410x_id'
LF_SEARCH = 'lf_search'
HF_SEARCH = 'hf_search'
WRITE_EM410X_CARD = 'write_em410x_card'
EMULATE_DESFIRE_ID = 'emulate_desfire_id'
EMULATE_EM410X_ID = 'emulate_em410x_id'
EMULATE_MF_CLASSIC_1K_ID = 'emulate_mf_classic_1k_id'
EMULATE_MF_CLASSIC_4K_ID = 'emulate_mf_classic_4k_id'
EMULATE_MF_ULTRALIGHT_ID = 'emulate_mf_ultralight_id'
LOAD_LEGIC_CARD = 'load_legic_card'
WRITE_LEGIC_CARD = 'write_legic_card'
EMULATE_LEGIC_CARD = 'emulate_legic_card'
ELOAD_LEGIC_CARD = 'eload_legic_card'
AUTOPWN_MF_CARD = 'autopwn_mf_card'
WRITE_MF_CARD = 'write_mf_card'
EMULATE_MF_CARD = 'emulate_mf_card'
ELOAD_MF_CARD = 'eload_mf_card'
LOAD_MF_ULTRALIGHT_CARD = 'load_mf_ultralight_card'
WRITE_MF_ULTRALIGHT_CARD = 'write_mf_ultralight_card'
EMULATE_MF_ULTRALIGHT_CARD = 'emulate_mf_ultralight_card'
ELOAD_MF_ULTRALIGHT_CARD = 'eload_mf_ultralight_card'
CHANGE_MF_CLASSIC_ID = 'change_mf_classic_id'
CHANGE_MF_ULTRALIGHT_ID = 'change_mf_ultralight_id'

# Legic Prime emulation types
MIM22 = 'mim22'
MIM256 = 'mim256'
MIM1024 = 'mim1024'

# MF Ultralight emulation types
MFU = 'mfu'
MFU_EV1 = 'mfu_ev1'

# EM410X encoding types
T55X7 = 't55x7'
Q5 = 'q5'
EM4305 = 'em4305'

# MF Classic magic generations
GEN1 = 'gen1'
GEN3 = 'gen3'

# Command reactions
MISSING_PM3 = 'missing_pm3'
MISSING_READER = 'missing_reader'
NOTHING = 'nothing'
NO_CARD_FOUND = 'no_card_found'
OUTPUT_HANDLED = 'output_handled'
UNKNOWN_OUTPUT = 'unknown_output'
PROBLEM = 'problem'
UNKNOWN_COMMAND = 'unknown_command'

# Waiting time
TOAST_DISAPPEAR_PERIOD = 9999
