"""
start_stop_visual_checks.py

Script to save the current participant's base file after performing visual checks before generating the next
participant's base sip file.

Author: Sam Pedersen
Date: 2023-08-02
"""

# ! python3
import scanip_api3 as sip
import sys

# Add module to path for importing
module_path = "P:\\WoodsLab\\ACT-head_models\\FEM\\Sam\\Scripts\\Python\\Simpleware\\quality_checking\\"
sys.path.append(module_path)

# Import quality checking module
import quality_check_functions as qc

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
- Note that currently, participants must belong to the same subgroup; future iterations of this code will update to 
    streamline across participant sublist groups/directories  

- Variables:
    - currently_opened_file: (Bool) Set this variable to be True or False to indicate if there is currently an sip file 
        opened within Simpleware (True) or not (False)
    - current_participant: (int) Set this variable as the current participant's 6-digit identifier (eg: 999999) 
    - next_participant: (int) Set this variable as the next participant's 6-digit identifier (eg: 888888)
    - sublist: (str) Set this variable to either be "v1", "v2", "v3", "ET_old", or "ET_new", depending on the sublist the 
        target participant belongs to  
        
########################################################################################################################
"""

"""
Folder locations: 
V1:
"P:\\WoodsLab\\ACT-head_models\\FEM\\manual_segmentation\\allParticipants\PL_v1\\"
V2:
"P:\\WoodsLab\\ACT-head_models\\FEM\\manual_segmentation\\allParticipants\PL_v2\\"
V3:
"P:\\WoodsLab\\ACT-head_models\\FEM\\manual_segmentation\\allParticipants\PL_v3\\"
ETold:
"P:\\WoodsLab\\ACT-head_models\\FEM\\manual_segmentation\\allParticipants\PL_ETold\\"
ETnew: 
"P:\\WoodsLab\\ACT-head_models\\FEM\\manual_segmentation\\allParticipants\PL_ETnew\\"
"""

currently_opened_file = True
# currently_opened_file = False                 # Example
current_participant = 999999
# current_participant = 102936                  # Example
sublist = "v1"
# sublist = "ET_old"                            # Example
next_participant = 888888
# next_participant = 199472                     # Example




folder_location = "INSERT\\FOLDER\\LOCATION\\HERE\\"


########################################################################################################################
# Execute the script

# Determine base directory location based on sublist
base_dir = "P:\\WoodsLab\\ACT-head_models\\FEM\\manual_segmentation\\allParticipants\\"
if sublist == "v1":
    base_location = f"{base_dir}PL_v1\\"
elif sublist == "v2":
    base_location = f"{base_dir}PL_v2\\"
elif sublist == "v3":
    base_location = f"{base_dir}PL_v3\\"
elif sublist == "ET_old":
    base_location = f"{base_dir}PL_ETold\\"
elif sublist == "ET_new":
    base_location = f"{base_dir}PL_ETnew\\"
else:
    qc.message_box("No directory found at the sublist specified. Please ensure that you entered either v1, v2, v3, "
                   "ET_old, or ET_new.")
    base_location = "None"
    exit()


# If there is a file currently opened in Simpleware...
if currently_opened_file:
    # Save and close the current file before generating the next participant's file
    qc.stop_start_visual_checks(current_participant, next_participant, base_location)
# If there is not a file currently opened in Simpleware...
else:
    # Generate the current participant's file and save it to their folder, leaving the file open
    qc.generate_base_file(current_participant, base_location)
