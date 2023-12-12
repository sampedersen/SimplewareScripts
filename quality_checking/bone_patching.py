"""
bone_patching.py

Automate pre-processing applications to bone mask for quality checking procedures.

Author: Sam Pedersen
Date: 2023-11-14
"""
########################################################################################################################
"""
Notes for use:

- patched_bone is the final patched bone mask to implement additional edits upon 
- unpatched_bone_regions indicates the areas that did not get patched 
- patched_bone_regions_raw indicates areas that received patch processing, before corrections
- patched_bone_regions_corrected indicates areas that received patch processing, following corrections
- Edits will be derived from whichever mask is called "bone"; original mask and properties will be preserved and 
    untouched
    
- Please specify the participant's 6-digit identifier in the variable participant_id
- Please specify the sublist the participant belongs to in the variable sublist  
- Please specify if this project file needs the Binarized_masks/final/bone.raw file imported or not using the 
    import_bone variable
    - import_bone = False if you do not need it imported
    - import_bone = True if you do need it imported 
    
Ensure that the pre-existing masks in your .sip file do not have any of the following names:
- Copy of bone
- bone_old 
- patched_bone
- unpatched_bone_regions
- patched_bone_regions_raw
- patched_bone_regions_corrected
If you have a naming conflict, rename the pre-existing mask to be at least 1 character different 

"""
########################################################################################################################

participant_id = 999999
# participant_id = 100220       # Example
sublist = "v3"
# sublist = "v1"                # Example
import_bone = False
# import_bone = True            # Example

########################################################################################################################

# Import necessary packages
# ! python3
import scanip_api3 as sip
import sys
# Add module to path for importing
module_path = "P:\\WoodsLab\\ACT-head_models\\FEM\\Sam\\Scripts\\Python\\Simpleware\\quality_checking\\"
sys.path.append(module_path)
# Import quality checking module
from lib.functions import quality_check_functions as qc

########################################################################################################################

# Execute script functions
if import_bone == True:
    # Import bone if needed; importing from Binarized_masks\final
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
    mask_folder = f"{participant_folder}\\Binarized_masks\\final\\"
    qc.import_mask("bone",mask_folder)
    sip.App.GetDocument().GetGenericMaskByName("bone_old").SetName("bone")
qc.bone_patching()