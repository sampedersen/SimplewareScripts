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
# directory = "P:\\ACT-head_models\\FEM\\manual_segmentation\\Participant_list_v3\\idvParticipants\\"
directory = "Z:\\ACT-head_models\\FEM\\manual_segmentation\\Participant_list_v3\\idvParticipants\\"


# Participants to generate files for:
participants = [100400, 100905, 100910]
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
    # Headreco folder
    headrecoFolder = subjPathway + "headreco\\" 
    # Headreco file
    headreco = headrecoFolder + "FS6.0_sub-" + str(SUBJ_ID) + "_ses-01_T1w_masks_contr.RAW" 

    

    # Generate project file
    App.GetInstance().ImportRawImage(subjPathway + "T1.raw", ImportOptions.DoublePixel, 256, 256, 256, 1, 1, 1, 0,
                                     ImportOptions.BinaryFile, ImportOptions.LittleEndian,
                                     CommonImportConstraints().SetWindowLevel(0, 0).SetCrop(0, 0, 0, 256, 256,
                                                                                            256).SetPixelType(
                                         Doc.Float32))
    # Rename background to <SUBJECT_NUMBER>_T1
    App.GetDocument().GetBackgroundByName("Raw import [W:0.00 L:0.00]").SetName(str(SUBJ_ID) + "_T1")


    # Import and threshold headreco
    App.GetInstance().GetActiveDocument().ImportBackgroundFromRawImage(headreco, ImportOptions.DoublePixel, 256, 256,
                                                                       256, 1, 1, 1, 0, ImportOptions.BinaryFile,
                                                                       ImportOptions.LittleEndian,
                                                                       CommonImportConstraints().SetWindowLevel(0, 0).SetCrop(0, 0, 0, 256, 256, 256).SetPixelType(Doc.Float32))
    # Rename background to <SUBJECT_NUMBER>_headreco
    App.GetDocument().GetBackgroundByName("Raw import [W:0.00 L:0.00]").SetName(str(SUBJ_ID) + "_headreco")

    # Activate headreco as background
    App.GetDocument().GetBackgroundByName(str(SUBJ_ID) + "_headreco").Activate()

    # Threshold whitematter [1, 1]
    App.GetDocument().Threshold(1, 1, Doc.CreateNewMask, App.GetDocument().GetSliceIndices(Doc.OrientationXY),
                                Doc.OrientationXY)
    App.GetDocument().ApplyCavityFillFilter()
    App.GetDocument().ApplyBinarisationFilter()
    App.GetDocument().GetGenericMaskByName("Mask 1").SetName("headreco_wm")

    # Threshold greymatter [2, 2]
    App.GetDocument().Threshold(2, 2, Doc.CreateNewMask, App.GetDocument().GetSliceIndices(Doc.OrientationXY),
                                Doc.OrientationXY)
    App.GetDocument().ApplyCavityFillFilter()
    App.GetDocument().ApplyBinarisationFilter()
    App.GetDocument().GetGenericMaskByName("Mask 1").SetName("headreco_gm")

    # Threshold CSF [3, 3]
    App.GetDocument().Threshold(3, 3, Doc.CreateNewMask, App.GetDocument().GetSliceIndices(Doc.OrientationXY),
                                Doc.OrientationXY)
    App.GetDocument().ApplyCavityFillFilter()
    App.GetDocument().ApplyBinarisationFilter()
    App.GetDocument().GetGenericMaskByName("Mask 1").SetName("headreco_csf")

    # Threshold bone [4, 4]
    App.GetDocument().Threshold(4, 4, Doc.CreateNewMask, App.GetDocument().GetSliceIndices(Doc.OrientationXY),
                                Doc.OrientationXY)
    App.GetDocument().ApplyCavityFillFilter()
    App.GetDocument().ApplyBinarisationFilter()
    App.GetDocument().GetGenericMaskByName("Mask 1").SetName("headreco_bone")

    # Threshold skin [5, 5]
    App.GetDocument().Threshold(5, 5, Doc.CreateNewMask, App.GetDocument().GetSliceIndices(Doc.OrientationXY),
                                Doc.OrientationXY)
    App.GetDocument().ApplyCavityFillFilter()
    App.GetDocument().ApplyBinarisationFilter()
    App.GetDocument().GetGenericMaskByName("Mask 1").SetName("headreco_skin")

    # Threshold air [6, 6]
    App.GetDocument().Threshold(6, 6, Doc.CreateNewMask, App.GetDocument().GetSliceIndices(Doc.OrientationXY),
                                Doc.OrientationXY)
    App.GetDocument().ApplyCavityFillFilter()
    App.GetDocument().ApplyBinarisationFilter()
    App.GetDocument().GetGenericMaskByName("Mask 1").SetName("headreco_air")

    # Save project
    App.GetDocument().SaveAs(sipFolder + str(SUBJ_ID) + "_Sam.sip")

    # Close the project file
    App.GetDocument().Close()
