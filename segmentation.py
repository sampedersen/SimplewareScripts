"""
segmentation.py

Module for implementing segmentation-related functions

This module contains functions for displaying a message within a dialogue box, verifies module importing to user,
standardized tissue mask colors, remove tissue overlap

Author: Sam Pedersen
Date: 23 July 2023

---------------------

Notes for use:
- This module's functions are intended to be use within Synopsys Simpleware ScanIP's scripting environment
- As is, these functions *cannot* be executed outside Simpleware or within alternative IDEs
- Simpleware's scripting environment will not re-import modules during the same session; if any edits are made to this
    module, exit Simpleware entirely and begin a new session. Otherwise, Simpleware will continue executing the version
    of the module originally imported
- This module is not intended for direct execution, only for external importing

"""


# Import operating system and Simpleware modules
import os
import scanip_api3 as sip


# Function to display message box
def message_box(msg):

    """

    Function to display a message within a pop-up dialogue box.

    Args:
        msg (str): Message to be displayed

    Returns:
        None

    """

    # Display dialogue box and message
    sip.App.GetInstance().ShowMessage(msg)


def verify_import():

    """

    Verifies to user that segmentation.py module was successfully imported to Simpleware environment

    Args:
        None

    Return:
        None

    """

    sip.App.GetInstance().ShowMessage("QCFunctions module imported successfully.")


def colors_visibility(mask):

    """

    Assigns colors to tissue masks based on name. If trying to change the color of multiple masks at a time, use a for
    loop.

    Args:
        mask (str): Name of the mask to switch colors; must match one of the keys below

    Return:
        None

    """

    # Establish a dictionary of tissue names and their associated RBG color codes
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

    # Select for tissue-specific color
    color = color_dict[mask]
    # Set color and make visible
    sip.App.GetDocument().GetActiveGenericMask().SetColour(sip.Colour(*color))
    sip.App.GetDocument().GetActiveGenericMask().SetVisible(True)


def separate_masks():

    """

    Separates/removes any overlapping/intersecting masks based on priority of tissues. Must have all 11 masks.

    Args:
        None

    Return:
        None

    """

    # Shorten naming structures
    app = sip.App.GetInstance()
    doc = app.GetDocument()
    sliceIndices = doc.GetSliceIndices(sip.Doc.OrientationXY)
    sliceOrientation = sip.Doc.OrientationXY

    # Perform removal of overlap
    # GM - WM
    doc.ReplaceMaskUsingBooleanExpression("(gm MINUS wm)", doc.GetMaskByName("gm"), sliceIndices, sliceOrientation)
    # WM - (eyes, csf)
    doc.ReplaceMaskUsingBooleanExpression("(wm MINUS eyes MINUS csf)", doc.GetMaskByName("wm"), sliceIndices,
                                          sliceOrientation)
    # air - (wm, gm, csf, blood, skin)
    doc.ReplaceMaskUsingBooleanExpression("(air MINUS wm MINUS gm MINUS csf MINUS blood MINUS skin)",
                                          doc.GetMaskByName("air"), sliceIndices, sliceOrientation)
    # blood - (wm, gm, eyes, skin)
    doc.ReplaceMaskUsingBooleanExpression("(blood MINUS wm MINUS gm MINUS eyes MINUS skin)", doc.GetMaskByName("blood"),
                                          sliceIndices, sliceOrientation)
    # cortical - (wm, gm, air, eyes, blood)
    doc.ReplaceMaskUsingBooleanExpression("(cortical MINUS wm MINUS gm MINUS air MINUS eyes MINUS blood)",
                                          doc.GetMaskByName("cortical"), sliceIndices, sliceOrientation)
    # cancellous - (wm, gm, air, eyes, blood)
    doc.ReplaceMaskUsingBooleanExpression("(cancellous MINUS wm MINUS gm MINUS air MINUS eyes MINUS blood)",
                                          doc.GetMaskByName("cancellous"), sliceIndices, sliceOrientation)
    # cortical - (skin, cancellous, csf)
    doc.ReplaceMaskUsingBooleanExpression("(cortical MINUS skin MINUS cancellous MINUS csf)", doc.GetMaskByName("gm"),
                                          sliceIndices, sliceOrientation)
    # cancellous - (skin, csf)
    doc.ReplaceMaskUsingBooleanExpression("(cancellous MINUS skin MINUS csf)", doc.GetMaskByName("cancellous"),
                                          sliceIndices, sliceOrientation)
    # fat - (skin, wm, gm, eyes, air, blood, cortical, cancellous, csf)
    doc.ReplaceMaskUsingBooleanExpression(
        "(fat MINUS skin MINUS wm MINUS gm MINUS eyes MINUS air MINUS blood MINUS cortical MINUS cancellous MINUS csf)",
        doc.GetMaskByName("fat"), sliceIndices, sliceOrientation)
    # muscle - (skin, wm, gm, eyes, air, blood, cortical, cancellous, csf, fat)
    doc.ReplaceMaskUsingBooleanExpression(
        "(muscle MINUS skin MINUS wm MINUS gm MINUS eyes MINUS air MINUS blood MINUS cortical MINUS cancellous MINUS csf MINUS fat)",
        doc.GetMaskByName("muscle"), sliceIndices, sliceOrientation)
    # eyes - skin
    doc.ReplaceMaskUsingBooleanExpression("(eyes MINUS skin)", doc.GetMaskByName("eyes"), sliceIndices,
                                          sliceOrientation)
    # csf - eyes
    doc.ReplaceMaskUsingBooleanExpression("(csf MINUS eyes)", doc.GetMaskByName("csf"), sliceIndices, sliceOrientation)




