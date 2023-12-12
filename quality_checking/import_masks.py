"""
import_masks.py

Script for importing individual tissue masks into the project file.

Author: Sam Pedersen
Date: 2023-08-03
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
- This script imports the specified participant's tissue masks 
- Ensure there is no background image in the .sip file named "Raw import [W:0.00 L:0.00]", or there may be errors
- Please edit the script when implementing within Simpleware, but please do not overwrite the P-drive template  

- Variables:
    - Examples below 
    - participant_id: Set this variable as the participant's 6-digit identifier (eg: 999999) 
    - sublist: Set this variable to either be "v1", "v2", "v3", "ET_old", or "ET_new", depending on the sublist the 
        target participant belongs to
    - masks: Set this list to be the masks you wish to import; refer to the bank below   
    - version: Set this variable to be "initial" or "final"; indicates whether to import from the Binarized_masks folder
        (initial) or the Binarized_masks/final folder (final)  

########################################################################################################################
"""

participant_id = 999999
# participant_id = 103485               # Example
sublist = "v1"
# sublist = "v3"                        # Example
masks = ["uniform","wm","gm","eyes","eyes interior","csf","air","blood","bone","cancellous",
         "cortical","skin","fat","muscle"]
# masks = ["fat","uniform","eyes"]      # Example
version = "initial"
# version = "final"                     # Example

########################################################################################################################

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

# Define path to participant's folder
participant_folder = f"{base_location}FS6.0_sub-{participant_id}_ses01\\"

# Define path to participant's tissue masks folder
if version == "final":
    mask_folder = f"{participant_folder}\\Binarized_masks\\final\\"
elif version == "initial":
    mask_folder = f"{participant_folder}\\Binarized_masks\\"
else:
    qc.message_box("No mask directory found at the location specified. Please ensure you entered either initial or final")
    exit()

# Import the listed masks
for mask in masks:
    qc.import_mask(mask,mask_folder)


