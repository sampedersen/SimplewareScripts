"""
start_stop_visual_checks.py

Script to save the current participant's base file after performing visual checks before generating the next
participant's base sip file.

Author: Sam Pedersen
Date: 2023-08-02
"""

# ! python3
import sys

# Add module to path for importing
module_path = "P:\\WoodsLab\\ACT-head_models\\FEM\\Sam\\Scripts\\Python\\Simpleware\\quality_checking\\"
sys.path.append(module_path)

# Import quality checking module
from lib.functions import quality_check_functions as qc

"""
########################################################################################################################
Notes for use: 
- This script streamlines the visual checking process by saving the current participant's base file to their folder
- It then closes the file and generates the next participant's base file, saving and opening it as well 
- Be careful implementing this script in succession; if the participant numbers are not updated between executions, 
    it may overwrite previously saved files 
- If there is no .sip file currently opened in Simpleware, use the currently_opened_file variable below to indicate
    - If there is no .sip file, the script will generate the initial sip file for the participant listed as 
        current_participant
    - If there is already a .sip opened, the script will close and save the file before generating and opening the next 
    
- Variables:
    - currently_opened_file: (Bool) Set this variable to be True or False to indicate if there is currently an sip file 
        opened within Simpleware
    - current_participant: (int) Set this variable as the current participant's 6-digit identifier (eg: 999999) 
    - next_participant: (int) Set this variable as the next participant's 6-digit identifier (eg: 888888)
    - folder_location: (str) Set this variable as the overall folder hosting the target participants' directories  

########################################################################################################################
"""


currently_opened_file = True
# currently_opened_file = False                         # Example
current_participant = 999999
# current_participant = 807290                          # Example
next_participant = 888888
# next_participant = 839782                             # Example
sublists = "v1"
# sublists = "v2"                                       # Example


########################################################################################################################
# Execute the script

# Determine base directory location based on sublist
base_dir = "P:\\WoodsLab\\ACT-head_models\\FEM\\manual_segmentation\\allParticipants\\"
if sublists == "v1":
    folder_location = f"{base_dir}PL_v1\\"
elif sublists == "v2":
    folder_location = f"{base_dir}PL_v2\\"
elif sublists == "v3":
    folder_location = f"{base_dir}PL_v3\\"
elif sublists == "ET_old":
    folder_location = f"{base_dir}PL_ETold\\"
elif sublists == "ET_new":
    folder_location = f"{base_dir}PL_ETnew\\"
else:
    qc.message_box("No directory found at the sublist specified. Please ensure that you entered either v1, v2, v3, "
                   "ET_old, or ET_new.")
    folder_location = "None"
    exit()

# Check that there is currently a file opened within Simpleware
if currently_opened_file:
    # If there is, perform the stop_start_visual_checks function
    qc.stop_start_visual_checks(current_participant, next_participant, folder_location)
else:
    # If there is not, perform the generate_base_file function for the current participant 
    qc.generate_base_file(current_participant, folder_location)
