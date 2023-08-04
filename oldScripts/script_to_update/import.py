# Import finalized tissue masks to current project file 
# Created by Samantha Pedersen (07/25/2022)
# Last updated: 07/25/2022

#! python3
from scanip_api3 import *

########################################################################################################################
###########################################       !!! README !!!         ###############################################
########################################################################################################################

# Script function: 
#   1. Import finalized tissue masks from participant folder as a background image in current file 
#   2. Rename background images to reflect their respective tissue type
#   3. Threshold background to generate mask 

# Notes:
#   - Be sure that the masks you intend to import exist within the participant's /final folder as a .RAW image
#   - If executed as-is, the script will import *all* tissues
#       - For selective importing, simply remove the tissues you do not want to import from the list of masks below 
#       - More info below (line 41)

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
directory = "Z:\\ACT-head_models\\FEM\\manual_segmentation\\Participant_list_v3\\idvParticipants\\"

subjFolder = "FS6.0_sub-" + str(SUBJ_ID) + "_ses01\\" 
subjPathway = directory + subjFolder
binMasks = subjPathway + "Binarized_masks\\"

# Masks to import:
# Note: The 'masks' variable below specifies *all* tissue masks for importing
# If you'd like to selective import certain tissues, remove the unnecessary tissues with their respective apostrophes/commas
#      Example, if you only want to import air and blood:
#      masks = ['air','blood']
masks = ['wm','gm','eyes','eyes interior','air','blood','bone','cancellous','cortical','skin','fat','muscle','uniform']
upperLimit = len(masks)

########################################################################################################################

for i in range (0,upperLimit):
    
    # Establish mask info 
    maskName = masks[i]
    importInfo = binMasks + maskName + '.raw'
    
    #Import tissue mask as background image 
    App.GetInstance().GetActiveDocument().ImportBackgroundFromRawImage(importInfo, ImportOptions.UnsignedCharPixel, 
                                                                    256, 256, 256, 1, 1, 1, 0, ImportOptions.BinaryFile, 
                                                                    ImportOptions.LittleEndian, 
                                                                    CommonImportConstraints().SetWindowLevel(0, 0).SetCrop(0, 0, 0, 256, 256, 256))

    
    # Rename background image to mask's name
    App.GetDocument().GetBackgroundByName("Raw import [W:0.00 L:0.00]").SetName(maskName)
    # Copy background image into mask
    App.GetDocument().CopyBackgroundToMask()
    # Delete imported background image
    App.GetDocument().RemoveBackground(App.GetDocument().GetBackgroundByName(maskName))

    i = i + 1

