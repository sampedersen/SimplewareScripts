# Import operating system and Simpleware modules
import os
import scanip_api3 as sip

""" 
quality_check_functions.py 

This module contains the functions used during the segmentation quality checking process. 

Author: Sam Pedersen
Date: 2023-07-20
"""


"""
########################################################################################################################

                                                !!! README !!!
- This module is intended for use within Synopsys Simpleware ScanIP's scripting environment
- These functions *cannot* be executed outside Simpleware or within alternative IDEs
- Simpleware's scripting environment will not re-import modules within the same session; if any edits are made to this
module, exit Simpleware entirely and begin a new session. Otherwise, Simpleware will continue executing the originally
imported version of the module
- If you need to import this module to the Simpleware scripting environment, you must first add the project folder to
the system path within Simpleware (see instructions below); this must also be repeated anytime the Simpleware session
is reset

#######################################################################################################################

List of functions:
    - messageBox()
    - testImporting()
    - importFiles()

Function purposes:
    - messagebox: Displays user message to dialogue window
    - testImporting: Confirms that QCFunctions module was properly imported by displaying dialogue window
    - importFiles: Generates participant's quality checking file (if T1 is available) and imports masks, saving sip file
    to quality check folder

How to import QCFunctions to Simpleware's scripting environment:
    - Copy and past the following lines to the scripting environment and execute the code
    - Replace <FULL:\\PATH\\T0\\PROJECT\\FILE\\> with the actual file path
    - Project file path must be re-added to the path anytime the Simpleware session is restarted
        - Make sure the file path is contained in quotations
        - Make sure backslashes (\) are doubled (\\; special character)
        - Make sure there are two backslashes at the end of the path

    - Format:
            #! python3
            import scanip_api3 as sip
            import sys

            module_path = "<FULL:\\PATH\\T0\\PROJECT\\FILE\\>"
            sys.path.append(module_path)

    - Example:
            #! python3
            import scanip_api3 as sip
            import sys

            module_path = "C:\\Users\\samanthapedersen\\PycharmProjects\\quality_checking\\"
            sys.path.append(module_path)
"""

"""

messageBox
    - Argument: msg (string type)
    - Displays the argument as a pop-up dialogue window in Simpleware. User must select "continue" for function to end.
    - Example of use: 
        message = "Hello world!" 
        QCFunctions.messageBox(message)
        # Outcome: Dialogue box that displays [Hello world!]
        
"""

def messageBox(msg):
    sip.App.GetInstance().ShowMessage(msg)

########################################################################################################################


""" 

testImporting
    - Argument: N/A
    - Displays pre-set text message within dialogue window in Simpleware to indicate that the QCFunctions module was 
    imported; user must select "continue" for function to end 
    - Example of use:
        QCFunctions.testImporting()
        # Outcome: Dialogue box that displays [QCFunctions module imported successfully.]

"""

def testImporting():
    sip.App.GetInstance().ShowMessage("QCFunctions module imported successfully.")


########################################################################################################################


"""

colorsOrderVisibility
    - Arguments: N/A
    - Assigns the 11 tissues to a set of colors and their respective order of appearance 
    - Example of use:
        qc.colorsOrderVisibility()
        # Outcome: Tissue masks color and order are corrected 

"""
def colorsOrderVisibility():

    # List of mask names
    masks = ["wm", "gm", "eyes", "csf", "air", "blood", "cancellous", "cortical", "skin", "fat", "muscle"]

    # Establish a dictionary for tissues and color codes
    color_dict = {
        "air": (65, 65, 65),
        "blood": (200, 0, 0),
        "cancellous": (22, 167, 11),
        "cortical": (0, 255, 0),
        "csf": (107, 220, 220),
        "eyes": (194, 230, 230),
        "fat": (239, 217, 151),
        "gm": (176, 176, 176),
        "muscle": (255, 64, 64),
        "skin": (140, 120, 83),
        "wm": (207, 221, 220),
    }

    # Establish order of tissues
    order_dict = {
        "air": 7,
        "blood": 6,
        "cancellous": 5,
        "cortical": 4,
        "csf": 8,
        "eyes": 9,
        "fat": 2,
        "gm": 10,
        "muscle": 1,
        "skin": 3,
        "wm": 11
    }

    for mask in masks:
        # Est variables
        name = mask
        color = color_dict[name]
        order = order_dict[name]

        # Select specific mask
        sip.App.GetDocument().GetGenericMaskByName(name).Activate()

        # Set color
        sip.App.GetDocument().GetActiveGenericMask().SetColour(sip.Colour(*color))

        # Set order
        sip.App.GetDocument().MoveMaskTo(sip.App.GetDocument().GetActiveGenericMask(), order)

        # Make visible
        sip.App.GetDocument().GetActiveGenericMask().SetVisible(True)


########################################################################################################################


"""

separateMasks
    - Arguments: N/A
    - Removes any overlap/intersection between masks based on priority of tissues 
    - Example of use:
        qc.separateMasks()
        # Outcome: Overlap between masks is removed via Boolean operations 

"""
def separateMasks():

    app = sip.App.GetInstance()
    doc = app.GetDocument()
    sliceIndices = doc.GetSliceIndices(sip.Doc.OrientationXY)
    sliceOrientation = sip.Doc.OrientationXY

    doc.ReplaceMaskUsingBooleanExpression("(gm MINUS wm)", doc.GetMaskByName("gm"), sliceIndices, sliceOrientation)
    doc.ReplaceMaskUsingBooleanExpression("(wm MINUS eyes MINUS csf)", doc.GetMaskByName("wm"), sliceIndices, sliceOrientation)
    doc.ReplaceMaskUsingBooleanExpression("(air MINUS wm MINUS gm MINUS csf MINUS blood MINUS skin)", doc.GetMaskByName("air"), sliceIndices, sliceOrientation)
    doc.ReplaceMaskUsingBooleanExpression("(blood MINUS wm MINUS gm MINUS eyes MINUS skin)", doc.GetMaskByName("blood"), sliceIndices, sliceOrientation)
    doc.ReplaceMaskUsingBooleanExpression("(cortical MINUS wm MINUS gm MINUS air MINUS eyes MINUS blood)", doc.GetMaskByName("cortical"), sliceIndices, sliceOrientation)
    doc.ReplaceMaskUsingBooleanExpression("(cancellous MINUS wm MINUS gm MINUS air MINUS eyes MINUS blood)", doc.GetMaskByName("cancellous"), sliceIndices, sliceOrientation)
    doc.ReplaceMaskUsingBooleanExpression("(cortical MINUS skin MINUS cancellous MINUS csf)", doc.GetMaskByName("gm"), sliceIndices, sliceOrientation)
    doc.ReplaceMaskUsingBooleanExpression("(cancellous MINUS skin MINUS csf)", doc.GetMaskByName("cancellous"), sliceIndices, sliceOrientation)
    doc.ReplaceMaskUsingBooleanExpression("(fat MINUS skin MINUS wm MINUS gm MINUS eyes MINUS air MINUS blood MINUS cortical MINUS cancellous MINUS csf)", doc.GetMaskByName("fat"), sliceIndices, sliceOrientation)
    doc.ReplaceMaskUsingBooleanExpression("(muscle MINUS skin MINUS wm MINUS gm MINUS eyes MINUS air MINUS blood MINUS cortical MINUS cancellous MINUS csf MINUS fat)", doc.GetMaskByName("muscle"), sliceIndices, sliceOrientation)
    doc.ReplaceMaskUsingBooleanExpression("(eyes MINUS skin)", doc.GetMaskByName("eyes"), sliceIndices, sliceOrientation)
    doc.ReplaceMaskUsingBooleanExpression("(csf MINUS eyes)", doc.GetMaskByName("csf"), sliceIndices, sliceOrientation)

########################################################################################################################


"""

importFiles
    - Arguments: participantID (integer type), folderLocation (string type)
        - participantID should be the participant's 6-digit identifier (ie, 999999 or 103485)
        - folderLocation should be the directory location that the participant's individual folder is contained within 
            - This is *not* the path *into* the participant's folder, but the path into the overall container 
            for all participants
            - Backslashes (\) must be doubled (\\; special character) 
            - Example: 
                - Path into participant's folder: P:\WoodsLab\...\manual_segmentation\FS6.0_sub-100893_ses01
                - folderLocation will be: P:\\WoodsLab\\...\\manual_segmentation\\ 
    - Performs the following functions:
        - Create a new sip file by loading in participant's T1.raw 
            - If the T1 is not available as FS6.0_sub-999999_ses01_T1_rs.RAW **OR** T1.RAW, the function will display a 
            dialogue box indicating that the T1 image could not be found 
            - The function will not perform the following actions until a T1 can be found 
        - Import tissue masks as background images, threshold into tissue masks
        - Places masks in correct order with agreeable colors  
        - Saves sip file to participant's quality check folder 
    - Example of use:
        QCFunctions.importFiles(999999,"P:\\segmentationParticipants\\")
        # Outcome: Generates a new sip file for 999999, importing T1 and tissue masks, saving to 
        P:\\segmentationParticipants\\999999Folder\\qualityChecks

"""

def importFiles(participantID, folderLocation):

    # Establish participant's folder and location
    participantFolder = folderLocation + "FS6.0_sub-" + str(participantID) + "_ses01\\"

    ### Check for T1.raw:
    # Participant's T1s usually exist within their base participant folder, but may exist in
    # potentially one of two formats:
    #   - FS6.0_sub-999999_ses01_T1_rs.RAW
    #   - T1.RAW
    # The following for loop will check if either of these versions exist in the participant's folder;
    # if one version exists, it will continue the following functions; if it is unable to find either version in the
    # participant's folder, it will skip to the else clause at the end to display the dialogue window

    ### Checking for T1.raw:
    # Preallocate T1 variable
    T1 = None
    # Naming structure, option 1
    t1Name1 = "FS6.0_sub-" + str(participantID) + "_ses01_T1_rs.RAW"
    # Naming structure, option 2
    t1Name2 = "T1.RAW"
    # List of T1 naming options (1 and 2)
    t1Names = [t1Name1, t1Name2]

    ### Check the T1 naming structure
    # For each naming option...
    for name in t1Names:
        # Identify T1_path as the full pathway to the participant's folder combined with each naming version
        T1_path = participantFolder + name
        # If a version of the T1 exists in the participant's folder...
        if os.path.exists(T1_path):
            T1 = T1_path        # ... set T1 to be the T1 path location and...
            break               # ... stop looking for a T1.

    ### If able to locate a T1 file:
    if T1:
        # Load the T1 into a new sip file
        sip.App.GetInstance().ImportRawImage(T1,
            sip.ImportOptions.DoublePixel, 256, 256, 256, 1.0, 1.0, 1.0, 0,
            sip.ImportOptions.BinaryFile, sip.ImportOptions.LittleEndian,
            sip.CommonImportConstraints().SetWindowLevel(0.0, 0.0).SetCrop(0, 0, 0, 256, 256, 256).SetPixelType(sip.Doc.Float32)
            )

        # Rename background image as 999999_T1
        sip.App.GetDocument().GetBackgroundByName("Raw import [W:0.00 L:0.00]").SetName(str(participantID) + "_T1")

        # Begin importing masks
        # Establish location for finalized masks from participant's folder
        maskLocation = participantFolder + "Binarized_masks\\idv_mask\\"
        # List of masks to be imported
        masks = ["wm","gm","eyes","csf","air","blood","cancellous","cortical","skin","fat","muscle"]

        ### For each mask in the list...
        for mask in masks:
            # ... Set the name as the particular mask...
            maskName = mask
            # ... Import info, combining the mask name and import source location...
            importInfo = maskLocation + maskName + ".raw"

            # ... Import tissue mask as background image...
            sip.App.GetInstance().GetActiveDocument().ImportBackgroundFromRawImage(
                importInfo,
                sip.ImportOptions.UnsignedCharPixel, 256, 256, 256, 1, 1, 1, 0,
                sip.ImportOptions.BinaryFile, sip.ImportOptions.LittleEndian,
                sip.CommonImportConstraints().SetWindowLevel(0, 0).SetCrop(0, 0, 0, 256, 256, 256)
                )
            # ... Rename background image to mask's name...
            sip.App.GetDocument().GetBackgroundByName("Raw import [W:0.00 L:0.00]").SetName(maskName)
            # ... Copy background image into mask...
            sip.App.GetDocument().CopyBackgroundToMask()
            # ... Delete imported background image
            sip.App.GetDocument().RemoveBackground(sip.App.GetDocument().GetBackgroundByName(maskName))

        ### Colors and order
        # Call the colorsOrderVisibility() function above
        colorsOrderVisibility()

        ### Save file as <999999>_QC1.sip to participant's quality checking folder
        qcSave = participantFolder + "qualityCheck\\sipFiles\\" + str(participantID) + "_QC1.sip"
        sip.App.GetDocument().SaveAs(qcSave)

    ### If the T1 was not able to be located, display a dialogue box indicating such
    else:
        messageBox("No RAW T1 scan found.")

########################################################################################################################


"""

exportFiles
    - Arguments: fileName (str), participantID (int), checkStage (int)
        - participantID should be the participant's 6-digit identifier (ex, 999999)
        - folderLocation should be the overall directory location that the individual's folder is housed within
        - checkStage should be a 1 or 2 to indicate if this is the end of QC1 or QC2 
    - Performs the following functions: 
        - Standardizes the colors/order/visibility of masks before removing potential overlap 
        - For each mask, binarizes and exports to the qualityCheck\\tisueMasks folder 
        - Saves the project to qualityCheck\\sipFiles as <999999>_QC<1 or 2>
    - Example of use: 
        - QCFunctions.exportFiles(999999, "P:\\segmentationParticipants\\",1)
        # Outcome: Binarizes and exports tissue masks to 
        P:\\segmentationParticipants\\999999Folder\\qualityCheck\\tissueMasks and saves the project file as 999999_QC1.sip
        to P:\\segmentationParticipants\\999999Folder\\qualityCheck\\sipFiles\\999999_QC1.sip
        

"""
def exportFiles(participantID,folderLocation,checkStage):

    # Establish participant's folder and location
    participantFolder = f"{folderLocation}FS6.0_sub-{participantID}_ses01\\qualityCheck\\"

    # Masks to binarize/export
    masks = ["wm", "gm", "eyes", "csf", "air", "blood", "cancellous", "cortical", "skin", "fat", "muscle"]

    # Standardize colors and order
    colorsOrderVisibility()
    # Separate masks
    separateMasks()

    # Binarize and export tissue masks
    for mask in masks:
        name = mask
        exportLocation = f"{participantFolder}tissueMasks\\"
        exportingMask = exportLocation + name + ".raw"


        # Binarize
        sip.App.GetDocument().GetGenericMaskByName(name).Activate()
        sip.App.GetDocument().ApplyBinarisationFilter()

        # Export the mask
        sip.App.GetDocument().GetMaskByName(name).RawExport(exportingMask)


    # Save project
    sip.App.GetDocument().SaveAs(f"{participantFolder}sipFiles\\{participantID}_QC{checkStage}.sip")


########################################################################################################################


"""

stopStart
    - Arguments: 
        - currentParticipant (int), nextParticipant (int), folderLocation (str), checkStage (int)
            - currentParticipant should be the current participant's 6-digit identifier (ex, 999999)
            - checkStage should be a 1 or 2, indicating if the current file is at stage 1 of quality checking or stage 2
            - nextParticipant should be the subsequent participant's 6-digit identifier (ex, 888888)
            - folderLocation should be the overall folder in which the individuals' folder are *both* contained
                - This script cannot currently be used for sets of participants in separate directories 
    - Performs the following functions:
        - Finishes up the QC process for the current participant (binarize/export/save)
        - Closes the current participant's file
        - Generates the next participant's QC1 file 
    - Example of use:
        QCFunctions.stopStart(999999, 2, 888888, "P:\\participantFolders\\") 
        # Outcome: Currently opened file for 999999 is saved as 999999_QC2.sip to 
        P:\\participantFolder\\999999Folder\\qualityCheck\\sipFiles and the tissue masks are binarized/exported to 
        P:\\participantFolder\\999999Folder\\qualityCheck\\tissueMasks ; once completed, 999999_QC2.sip is closed and
        888888_QC1.sip is generated within P:\\participantFolder\\888888Folder\\qualityCheck\\sipFiles
        
"""
def stopStart(currentParticipant, checkStage, nextParticipant, folderLocation):
    # Close out current file
    exportFiles(currentParticipant,folderLocation,checkStage)
    sip.App.GetDocument().Close()
    # Open next participant
    importFiles(nextParticipant,folderLocation)

