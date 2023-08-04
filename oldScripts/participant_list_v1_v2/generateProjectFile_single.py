# Generate a single new .sip project file 
# Created by Samantha Pedersen (09/30/2021)
# Last updated: 7/25/22
#! python3
from scanip_api3 import *

########################################################################################################################
########################################################################################################################



########################################################################################################################
###########################################       !!! README !!!         ###############################################
########################################################################################################################

# Script function:
#       1. Create a single new project file by importing paricipant's T1.raw
#           - If trying to create a batch of (mulitple) project files, use generateProjectFile_batch.py
#       2. Import and threshold participant's headreco output
#           - Generates an initial greymatter, whitematter, air, skin, and CSF masks
#       3. Save the file as <SUBJECT_ID>_<SEGMENTOR_NAME>.sip

# Notes:
#   - Be sure the participant has a pre-existing T1 and headreco file
#   - Files need to be in .RAW format prior to importing
#   - Script is meant to be run from Simpleware's opening interface, without any project being currently open

# !! IMPORTANT !!
# Change SUBJ_ID to match the participant's 6-digit identifier before executing script 
# Example:
# SUBJ_ID = 213456
SUBJ_ID = 999999

# !! IMPORTANT !!
# Change SEGMENTOR_NAME to be your name
# Example:
# SEGMENTOR_NAME = "Bobby"
SEGMENTOR_NAME = "<PUT_NAME_HERE>"

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
# Pathway to headreco folder 
headrecoFolder = subjPathway + "headreco\\"
# Pathway to sip_files folder 
sipFolder = subjPathway + "sip_files\\"

########################################################################################################################
######################################       Generate Project File     #################################################
########################################################################################################################

# Import the .raw T1 image as a background image
# 256x256x256, 64-bit (double)
App.GetInstance().ImportRawImage(subjPathway + "FS6.0_sub-" + str(SUBJ_ID) + "_ses01_T1_rs.raw", ImportOptions.DoublePixel, 256, 256, 256, 1, 1, 1, 0, ImportOptions.BinaryFile, ImportOptions.LittleEndian, CommonImportConstraints().SetWindowLevel(0, 0).SetCrop(0, 0, 0, 256, 256, 256).SetPixelType(Doc.Float32))
# Rename background to <SUBJECT_NUMBER>_T1
App.GetDocument().GetBackgroundByName("Raw import [W:0.00 L:0.00]").SetName(str(SUBJ_ID) + "_T1")

########################################################################################################################
#############################      Import and Threshold Headreco     ###################################################
########################################################################################################################

# Import headreco
App.GetInstance().GetActiveDocument().ImportBackgroundFromRawImage(headrecoFolder + "T1_T1orT2_masks.raw", ImportOptions.DoublePixel, 256, 256, 256, 1, 1, 1, 0, ImportOptions.BinaryFile, ImportOptions.LittleEndian, CommonImportConstraints().SetWindowLevel(0, 0).SetCrop(0, 0, 0, 256, 256, 256).SetPixelType(Doc.Float32))
# Rename background to <SUBJECT_NUMBER>_headreco
App.GetDocument().GetBackgroundByName("Raw import [W:0.00 L:0.00]").SetName(str(SUBJ_ID) + "_headreco")

# Activate headreco as background
App.GetDocument().GetBackgroundByName(str(SUBJ_ID) + "_headreco").Activate()

# Threshold whitematter [1, 1]
App.GetDocument().Threshold(1, 1, Doc.CreateNewMask, App.GetDocument().GetSliceIndices(Doc.OrientationXY), Doc.OrientationXY)
App.GetDocument().ApplyCavityFillFilter()
App.GetDocument().ApplyBinarisationFilter()
App.GetDocument().GetGenericMaskByName("Mask 1").SetName("headreco_wm")

# Threshold greymatter [2, 2]
App.GetDocument().Threshold(2, 2, Doc.CreateNewMask, App.GetDocument().GetSliceIndices(Doc.OrientationXY), Doc.OrientationXY)
App.GetDocument().ApplyCavityFillFilter()
App.GetDocument().ApplyBinarisationFilter()
App.GetDocument().GetGenericMaskByName("Mask 1").SetName("headreco_gm")

# Threshold CSF [3, 3]
App.GetDocument().Threshold(3, 3, Doc.CreateNewMask, App.GetDocument().GetSliceIndices(Doc.OrientationXY), Doc.OrientationXY)
App.GetDocument().ApplyCavityFillFilter()
App.GetDocument().ApplyBinarisationFilter()
App.GetDocument().GetGenericMaskByName("Mask 1").SetName("headreco_csf")

# Threshold bone [4, 4]
App.GetDocument().Threshold(4, 4, Doc.CreateNewMask, App.GetDocument().GetSliceIndices(Doc.OrientationXY), Doc.OrientationXY)
App.GetDocument().ApplyCavityFillFilter()
App.GetDocument().ApplyBinarisationFilter()
App.GetDocument().GetGenericMaskByName("Mask 1").SetName("headreco_bone")

# Threshold skin [5, 5]
App.GetDocument().Threshold(5, 5, Doc.CreateNewMask, App.GetDocument().GetSliceIndices(Doc.OrientationXY), Doc.OrientationXY)
App.GetDocument().ApplyCavityFillFilter()
App.GetDocument().ApplyBinarisationFilter()
App.GetDocument().GetGenericMaskByName("Mask 1").SetName("headreco_skin")

# Threshold air [6, 6]
App.GetDocument().Threshold(6, 6, Doc.CreateNewMask, App.GetDocument().GetSliceIndices(Doc.OrientationXY), Doc.OrientationXY)
App.GetDocument().ApplyCavityFillFilter()
App.GetDocument().ApplyBinarisationFilter()
App.GetDocument().GetGenericMaskByName("Mask 1").SetName("headreco_air")


########################################################################################################################
#############################       Save as <SUBJ_ID>_<SEGMENTOR_NAME>.sip       #######################################
########################################################################################################################

# Save project as <SUBJECT_NUMBER>_Sam.sip
App.GetDocument().SaveAs(sipFolder + str(SUBJ_ID) + "_" + SEGMENTOR_NAME + ".sip")


