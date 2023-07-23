"""
segmentation.py

Module for implementing segmentation-related functions

This module contains functions for

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

    :param msg:
    :return:
    """