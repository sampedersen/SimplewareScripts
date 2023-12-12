"""
QC2_priming.py

Script to perform Quality Check #2 priming procedures by importing the original idv_masks and creating comparison masks
    to display edits made during QC1 process.

Author: Sam Pedersen
Date: 2023-12-06

########################################################################################################################

Notes for use:
    - This script will re-import the idv_masks and generate comparison masks before saving the file
    - Specify the participant's 6-digit ID
    - Also specify which of the masks were edited and require further comparisons

Variables:
    - Examples below


########################################################################################################################
"""
# Specify target subject's numbers
participant_id = 999999
# participant_id = 100300                               # Example

# Specify the subgroup the participant belongs to
sublist = "v1"
# sublist = "v3"                                        # Example

# Specify the edited masks requiring comparisons to original masks
edited_masks = [
    "muscle",
    "fat",
    "skin",
    "bone"
    "cortical",
    "cancellous",
    "blood",
    "air",
    "csf",
    "eyes",
    "gm",
    "wm"
]
# edited_masks = ["muscle","cancellous","cortical"]      # Example
########################################################################################################################
# Execute the script
# Please do not edit beyond this point (or do so at your own risk)

# ! python3
import sys

# Add module to path for importing
module_path = "P:\\WoodsLab\\ACT-head_models\\FEM\\Sam\\Scripts\\Python\\Simpleware\\quality_checking\\"
sys.path.append(module_path)

# Import quality checking module
from lib.functions import quality_check_functions as qc
import scanip_api3 as sip

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
    sys.exit(1)

masks = ["muscle","fat","skin","cortical","cancellous","blood","air","csf","eyes","gm","wm"]

# Save file as 999999_QC2.sip
save_as = f"{folder_location}FS6.0_sub-{participant_id}_ses01\\qualityCheck\\sipFiles\\{participant_id}_QC2_preprocess.sip"
sip.App.GetDocument().SaveAs(save_as)

# Import original idv masks
for mask in masks:
    qc.qc2_importing(mask, participant_id, folder_location)
# Regenerate the original bone mask from the canc/cort idv masks
qc.regen_bone()
# Perform Boolean operations to produce comparison masks
for edited_mask in edited_masks:
    qc.qc2_preproccessing(edited_mask)
# Move and set colors
qc.qc2_preproc_colors_order(edited_masks)

