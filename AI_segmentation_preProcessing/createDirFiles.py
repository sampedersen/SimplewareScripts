# Import os functions
import os

########################################################################################################################
# Create a function for creating directories using os functions
# argument = directory (with full path location) to be made
def createDirectory(directory):
    # If the directory does not already exist...
    if not os.path.exists(directory):
        # Create the directory
        os.makedirs(directory)
        # Print confirmation
        print("Created: ", directory)
    # If the directory already exists...
    else:
        # Do not do anything, simply notify that directory was not generated
        print("Could not create (already exists): ", directory)

########################################################################################################################

# Declare variable, base information for later

# Base directory location
baseDir = "P:\\WoodsLab\\ACT-head_models\\FEM\\manual_segmentation\\"

# List of participants needing additional directories added to pre-existing folders
participantNumbers = [
    105256,105601,105971,107802,109021,110081,202251,202808,203846,
    300700,301112,301428,301513,301538,303009,303346,115991,303673
]

########################################################################################################################

# For each participant in the list:
for i in range(len(participantNumbers)):

    # Establish participant's full file location
    location = baseDir + "FS6.0_sub-" + str(participantNumbers[i]) + "_ses01\\"
    # Establish location for qualityCheck folder
    qualityCheck = location + "qualityCheck\\"
    # Establish location for tissueMasks folder
    tissueMasks = qualityCheck + "tissueMasks\\"
    # Establish location for sipFiles folder
    sipFiles = qualityCheck + "sipFiles\\"

    # List of new directories to be generated
    newDirectories = [
        qualityCheck,
        tissueMasks,
        sipFiles
    ]

    # Execute createDirectory function to create empty folders as named in newDirectories
    for directory in newDirectories:
        createDirectory(directory)