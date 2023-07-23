# Binarize and export tissue masks before saving the file
# Created by Samantha Pedersen (09/09/2021)
# Last updated: 10/12/2021
#! python3
from scanip_api3 import *

########################################################################################################################
###########################################       !!! README !!!         ###############################################
########################################################################################################################

# Script function:
#   1. Binarize and export each mask
#   2. Saves file as <SUBJ_NUMBER>_Final.sip

# Masks to export (ensure these exist within the project file) 
#   - "wm"
#   - "gm"
#   - "eyes"
#   - "csf"
#   - "air"
#   - "blood"
#   - "bone"
#   - "cancellous"
#   - "cortical"
#   - "skin"
#   - "fat"
#   - "muscle"
#   - "uniform"

# !! IMPORTANT !!
# Change SUBJ_ID to match the participant's 6-digit identifier before executing script 
# Example:
# SUBJ_ID = 213456
SUBJ_ID = 999999

########################################################################################################################

# Note: Some user operate within the Z-drive and some operate within the P-drive
# The code below indicates the Z-drive; if you are using the P-drive, simply replace Z:\\ with P:\\
# Example:
# directory = "P:\\ACT-head_models\\FEM\\manual_segmentation\\"
directory = "Z:\\ACT-head_models\\FEM\\manual_segmentation\\"

# Participant folder
subjFolder = "FS6.0_sub-" + str(SUBJ_ID) + "_ses01\\"
# Pathway to participant folder
subjPathway = directory + subjFolder
# Pathway to Binarized_masks folder
binarizedMasks = subjPathway + "Binarized_masks\\"
# Pathway to sip_files folder 
sipFolder = subjPathway + "sip_files\\"


masks = ['mask_name_here']
upperLimit = len(masks)

########################################################################################################################

# Binarize and export tissue masks using a for loop
for i in range (0,upperLimit):
    # Establish mask info
    maskName = masks[i]
    exportInfo = binarizedMasks + maskName + '.raw'
    
    # Binarize
    App.GetDocument().GetGenericMaskByName(maskName).Activate()
    App.GetDocument().ApplyBinarisationFilter()
    
    # Export
    App.GetDocument().GetMaskByName(maskName).RawExport(exportInfo)
    i = i+1

# Save project as <subj_number>_Final.sip
App.GetDocument().SaveAs(sipFolder + str(SUBJ_ID) + "_Sam.sip")
