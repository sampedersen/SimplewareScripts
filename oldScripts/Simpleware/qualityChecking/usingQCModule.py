#! python3
import scanip_api3 as sip
import sys

module_path = "C:\\Users\\samanthapedersen\\PycharmProjects\\quality_checking\\"
sys.path.append(module_path)

import QCFunctions as qc

########################################################################################################################

checkModuleImport = True

if checkModuleImport:
    qc.verify_import()

########################################################################################################################

# Participant and directory info

# Participant ID (just the 6-digit identifier)
# Example:
#   participantID = 999999
participantID = 100031

# Participant directory 
# This should be the overall directory that houses *all* the individual participant folders 
# !!! NOTE !!! This variable *MUST* have double backslashes (\\) (this is a special coding character) and the variable *MUST* end with a set of backslashes too
# Example:
#   If 999999 and 888888 are both contained within P:\miscFolder\everyone then the variable would be: 
#       folderLocation = "P:\\miscFolder\\everyone\\"
#folderLocation ="P:\\WoodsLab\\ACT-head_models\\FEM\\manual_segmentation\\allParticipants\\PL_v1\\"
folderLocation = "C:\\Users\\samanthapedersen\\Desktop\\test\\"

# QC stage
# This variable should either be 1 or 2 
# This is only relevent when exporting/saving
# Set the variable as 1 if you are beginning/completing QC1
# Set the variable to 2 if you are beginning/completing QC2
checkStage = 2

# Next participant
# This should be the next participant for whom you want to begin the QC process for next 
# This is only relavent when exporting/saving current participant and then generating the next participant 
# 6-digit identifier 
nextParticipant = 100283

########################################################################################################################

# Call the functions
# Functions are commented out by default to avoid performing unintended functions
# Remove the comment hash (#) from pertinent lines of code to enable execution 

# Primary functions 
#qc.importFiles(participantID,folderLocation)
#qc.exportFiles(participantID,folderLocation,checkStage)
qc.stop_start_visual_checks(participantID, checkStage, nextParticipant, folderLocation)

# Secondary functions
#message = "Insert message you want to display here."
#qc.messagebox(message)
#qc.colorsOrderVisibility()
#qc.separateMasks()


