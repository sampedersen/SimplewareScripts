"""
generate_base_file.py

Script for generating the initial quality check #1 file.

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
- This script creates a new .sip file by loading the participant's T1.RAW image, imports the final tissue masks, sets 
    the masks' colors and order, and saves the files as <participant_id>_base.sip to their quality check folder
- There cannot be a currently opened project file already loaded into Simpleware when running this; close it first. 
- Final tissue masks must pre-exist in the participant's Binarized_masks/idv_masks folder 
- T1.RAW must be in the participant's overall folder; script will end and notify the user if the T1 cannot be found
- Depending on the version of Simpleware, the participant's quality checking folder may need to be pre-established; 
    newer versions will create the folder implicitly 
    - Quality check folder structures:
        <participant_folder>/qualityCheck/sipFiles
        <participant_folder>/qualityCheck/tissueMasks

- Variables:
    - Examples are below 
    - participant_id: (int) Set this variable as the participant's 6-digit identifier (eg: 999999)
    - sublist: (str) Set this to be either "v1", "v2", "v3", "ET_old", or "ET_new", depending on the participant 
        sublist your target belongs to      

########################################################################################################################
"""


participant_id = 999999
# Example:
# participant_id = 103495

sublist = "v0"
# Example:
# sublist = "v1"
# sublist = "ET_old"



########################################################################################################################
# Execute the script:

# Determine import directory location depending on specified sublist
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

# Call the function to import from the specified participant's folder and generate the base.sip file
qc.generate_base_file(participant_id, folder_location)
