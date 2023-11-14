"""
binarizeExportSave.py

Automating the process for binarizing & exporting tissue masks before saving file.

Note: Update in progress
Improving for flexibility across subgroups and directory locations.

Author: Sam Pedersen
Date: 2021-09-09
"""









########################################################################################################################
###########################################       !!! README !!!         ###############################################
########################################################################################################################

# Script function:
#   1. Binarize and export each mask
#   2. Saves file as <SUBJ_NUMBER>_Final.sip
# Masks to export: (must exist within project file):
#   - "wm", "gm", "eyes", "csf", "air", "blood", "bone", "cancellous", "cortical", "skin", "fat", "muscle", "uniform"

# Identify the following variables:
subj_id = "999999"
subgroup = "v1"
stage = "initial"
segmentor = "Sam"
drive = "P"


#! python3
from scanip_api3 import *

########################################################################################################################

# Establish drive assignment, either P-drive or Z-drive
mid_dir = "drive\\"
base_dir = "preallocating"

if drive == "P":
    base_dir = "P:\\"
elif drive == "Z":
    base_dir = "Z:\\"
participants = "%s%s%s\\"% (base_dir,mid_dir,subgroup)
participant = "%s%d"
directory = "Z:\\ACT-head_models\\FEM\\manual_segmentation\\Education_Training\\"

# Participant folder
subjFolder = "FS6.0_sub-" + str(subj_id) + "_ses01\\"
# Pathway to participant folder
subjPathway = directory + subjFolder
# Pathway to Binarized_masks folder
binarizedMasks = subjPathway + "Binarized_masks\\"
# Pathway to sip_files folder 
sipFolder = subjPathway + "sip_files\\"
# Pathway to final folder
final = binarizedMasks + "final\\"

masks = ['wm','gm','eyes','csf','air','blood','cancellous','cortical','skin','fat','muscle']
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
App.GetDocument().SaveAs(sipFolder + str(subj_id) + "_" + segmentor + ".sip")
