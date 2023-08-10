"""
finalize_sip_file.py

Script to finalize the quality checking process at either stage 1 or stage 2.

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
- This script finalizes the .sip file in either the quality check #1 or quality check #2, standardizing the 
    colors/order/visibility of the  masks before removing overlap, binarizing the masks, and exporting them to the 
    quality checking tissue mask folder before saving the .sip file 
- Intended to be implemented on the final 11 tissue masks, wm, gm, eyes, csf, air, blood, cancellous, cortical, skin, 
    fat, and muscle
- All tissue masks in the project file must have lower case names and match the spelling exactly
- If there is a masks missing, the script will stop; if there are additional masks beyond the 11 listed above, it will
    not be effected by the script
- Depending on the version of Simpleware, the participant's quality checking folder may need to be pre-established; 
    newer versions will create the folder implicitly 
    - Quality check folder structures:
        <participant_folder>/qualityCheck/sipFiles
        <participant_folder>/qualityCheck/tissueMasks 
    
- Variables:
    - Examples below
    - participant_id: (int) Set this variable as the participant's 6-digit identifier (eg: 999999) 
    - sublist : (str) Set this variable to either be "v1", "v2", "v3", "ET_old", or "ET_new", depending on the sublist the 
        target participant belongs to    
    - check_stage: (int) Set this variable as either 1 or 2, indicating if quality check #1 or quality check #2 is 
        being finalized

########################################################################################################################
"""


participant_id = 999999
# participant_id = 103294               # Example
sublist = "v1"
# sublist = "v3"                        # Example
check_stage = 1
# check_stage = 2                       # Example


########################################################################################################################
# Execute the script

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
    exit()

# Finalize the sip file by exporting and saving to the specified participant's folder, either as QC1 or QC2
qc.finalize_sip_file(participant_id, folder_location, check_stage)
