# Binarize and export tissue masks before saving the file
# Created by Samantha Pedersen (10/12/2021)
# Last updated: 11/17/2022
#! python3
from scanip_api3 import *

########################################################################################################################
###########################################       !!! README !!!         ###############################################
########################################################################################################################

# Script function:
#   1. Binarize and export each mask
#   2. Save the file as <SUBJ_NUMBER>_checked_<1 or 2>.sip

# Masks being used (make sure these exist in the project file):
#   - "wm"
#   - "gm"
#   - "eyes"
#   - "csf"
#   - "air"
#   - "blood"
#   - "cancellous"
#   - "cortical"
#   - "skin"
#   - "fat"
#   - "muscle"

# !! IMPORTANT !!
# Change SUBJ_ID to match the participant's 6-digit identifier before executing script 
# Example:
# SUBJ_ID = 213456
SUBJ_ID = 999999

# !! IMPORTANT !! 
# If you are conducting check_1, set checker_1 to be True.
#     - This will designate the file to be saved as <SUBJ_ID>_checked_1.sip
# If you are conducting check_2, set checker_1 to be False.
#     - This will designate the file to be saved as <SUBJ_ID>_checked_2.sip
checker_1 = True

# !! Important !! 
# Change INITIALS to match your initials 
INITIALS = "NA"

########################################################################################################################

# NOTE: This version of the script is intended for participant list_V3


# Note: Some user operate within the Z-drive and some operate within the P-drive
# The code below indicates the Z-drive; if you are using the P-drive, simply replace Z:\\ with P:\\
# Example:
# directory = "P:\\ACT-head_models\\FEM\\manual_segmentation\\Participant_list_v3\\idvParticipants\\"
directory = "Z:\\ACT-head_models\\FEM\\manual_segmentation\\Participant_list_v3\\idvParticipants\\"

# Participant folder
subjFolder = "FS6.0_sub-" + str(SUBJ_ID) + "_ses01\\"
# Pathway to participant folder
subjPathway = directory + subjFolder
# Pathway to Binarized_masks folder
binarizedMasks = subjPathway + "Binarized_masks\\"
# Pathway to sip_files folder 
sipFolder = subjPathway + "sip_files\\"
# Pathway to idv_mask folder
idv_mask = binarizedMasks + "idv_mask\\"

masks = ['wm','gm','eyes','csf','air','blood','cancellous','cortical','skin','fat','muscle']
upperLimit = len(masks)

########################################################################################################################
    
# Save file, binarize, export save 
if checker_1:
    # Binarize and export masks 
    for i in range(0,upperLimit):
        maskName = masks[i]
        exportInfo = idv_mask + maskName + '.raw'

        # Binarize
        App.GetDocument().GetGenericMaskByName(maskName).Activate()
        App.GetDocument().ApplyBinarisationFilter()
        # Export
        App.GetDocument().GetMaskByName(maskName).RawExport(exportInfo)
        i = i + 1
    App.GetDocument().SaveAs(sipFolder + str(SUBJ_ID) + "_checked_1_" + INITIALS + ".sip")
else:
    App.GetDocument().SaveAs(sipFolder + str(SUBJ_ID) + "_checked_2_" + INITIALS + ".sip")
