"""
segmentation.py

Module for implementing segmentation-related functions

This module contains functions for displaying a message within a dialogue box, verifies module importing to user,
standardized tissue mask colors,

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

