# Generate a batch of new .sip project files 
# Created by Samantha Pedersen (09/30/2021)
# Last updated: 7/25/22
#! python3
from scanip_api3 import *

########################################################################################################################
###########################################       !!! README !!!         ###############################################
########################################################################################################################

# Script function:
#   - Using a list of participant IDs, for loops through the IDs to establish initial project files
#   - Entails:
#       - Importing participant's T1 image
#       - Importing participant's headreco data
#       - Thresholds headreco masks
#       - Saves project file and closes
#       - Repeats until participant list is exhausted

# Notes:
#   - Requires participant numbers to be input as a comma-dilineated Python list (more info below)
#   - Be sure the participant has a pre-existing T1 and headreco file
#   - Files need to be in .RAW format prior to importing

########################################################################################################################
# Note: Some user operate within the Z-drive and some operate within the P-drive
# The code below indicates the Z-drive; if you are using the P-drive, simply replace Z:\\ with P:\\
# Example:
# directory = "P:\\ACT-head_models\\FEM\\manual_segmentation\\"
directory = "Z:\\ACT-head_models\\FEM\\manual_segmentation\\Education_Training\\"

# Participants to generate files for:
participants = [100835, 101342, 101644, 101886, 300352, 300390, 300609, 300646, 
    300654, 300891, 300976, 301051, 301079, 301099, 301217, 301293, 301528, 301571, 301586, 301660]
upperLimit = len(participants)

########################################################################################################################

for i in range (0,upperLimit):
    
    # Retrieve subject ID
    SUBJ_ID = participants[i]                              
    # Participant folder
    subjFolder = "FS6.0_sub-" + str(SUBJ_ID) + "_ses01\\"   
    # Full subject folder pathway
    subjPathway = directory + subjFolder                  
    # Path to sip file folder
    sipFolder = subjPathway + "sip_files\\"               
    # Headreco
    headreco = subjPathway + "T1_T1orT2_masks.raw"       
  

    

    # Generate project file
    App.GetInstance().ImportRawImage(subjPathway + "T1.raw", ImportOptions.DoublePixel, 256, 256, 256, 1, 1, 1, 0,
                                     ImportOptions.BinaryFile, ImportOptions.LittleEndian,
                                     CommonImportConstraints().SetWindowLevel(0, 0).SetCrop(0, 0, 0, 256, 256,
                                                                                            256).SetPixelType(
                                         Doc.Float32))
    # Rename background to <SUBJECT_NUMBER>_T1
    App.GetDocument().GetBackgroundByName("Raw import [W:0.00 L:0.00]").SetName(str(SUBJ_ID) + "_T1")


    # Save project
    App.GetDocument().SaveAs(sipFolder + str(SUBJ_ID) + "_initialFile.sip")

    # Close the project file
    App.GetDocument().Close()
