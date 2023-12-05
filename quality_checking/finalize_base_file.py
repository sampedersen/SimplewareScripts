"""
finalize_base_file.py

Script to finalize the initial base file (999999_base.sip) following implementation of primary edits and prior to
finalizing the overall QC1 step.

Author: Sam Pedersen
Date: 2023-12-05

########################################################################################################################

Notes for use:
- This script finalizes the .sip file in after implementing primary edits by generating cancellous/cortical tissues
    (optional), generating eyes interior (optional), resetting the colors/order, remove pre-existing muscle/csf,
    and save the file as 999999_base.sip
- Intended to be implemented on the final 11 tissue masks, wm, gm, eyes, csf, air, blood, cancellous, cortical, skin,
    fat, and muscle
- If conducting cancellous/cortical tissue regeneration, script additionally requires a "threshold" mask
- All tissue masks in the project file must have lower case names and match the spelling exactly
- If there is a masks missing, the script will stop; if there are additional masks beyond the 11 listed above, they will
    not be effected by the script

Variables:
    - Examples below
    - participant_id: (int) Set this variable as the participant's 6-digit identifier (eg: 999999)
    - sublist : (str) Set this variable to either be "v1", "v2", "v3", "ET_old", or "ET_new", depending on the sublist
        the target participant belongs to
    - regen_bone: (Boolean) Set to True/False to include regeneration of cancellous/cortical masks stages
    - regen_eyes_int: (Boolean) Set to True/False to include regeneration of eyes interior stages

"""
########################################################################################################################

participant_id = 999999
# participant_id = 103294               # Example
sublist = "v1"
# sublist = "v3"                        # Example
regen_bone = True
# regen_bone = False                    # Example
regen_eyes_int = True
# regen_eyes_int = False                # Example

########################################################################################################################
# Execute the script
# Please do not edit beyond this point (or do so at your own risk)

# ! python3
import sys

# Add module to path for importing
module_path = "P:\\WoodsLab\\ACT-head_models\\FEM\\Sam\\Scripts\\Python\\Simpleware\\quality_checking\\"
sys.path.append(module_path)

# Import quality checking module
import quality_check_functions as qc

# Determine base directory location based on sublist
base_dir = "P:\\WoodsLab\\ACT-head_models\\FEM\\manual_segmentation\\allParticipants\\"
if sublist == "v1":
    folder_location = f"{base_dir}PL_v1\\"
elif sublist == "v2":
    folder_location = f"{base_dir}PL_v2\\"
elif sublist == "v3":
    folder_location = f"{base_dir}PL_v3\\"
elif sublist == "ET_old":
    folder_location = f"{base_dir}PL_ETold\\"
elif sublist == "ET_new":
    folder_location = f"{base_dir}PL_ETnew\\"
else:
    qc.message_box("No directory found at the sublist specified. Please ensure that you entered either v1, v2, v3, "
                   "ET_old, or ET_new.")
    folder_location = "None"
    exit()

# Finalize the base sip file
qc.finalize_base_sip(participant_id, folder_location, regen_bone, regen_eyes_int)
