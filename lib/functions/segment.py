import scanip_api3 as sip

# Boolean functions
def boolean_operation(mask_a, mask_b, operation):
    """

    Function to perform boolean operations between two masks. Performs operations to mask_a.

    Args:
        mask_a:
        mask_b:
        operation: (str) Determine which Boolean operation to perform.


    Returns:

    """
    if operation == "subtract":
        boolean_setting = f"({mask_a} MINUS {mask_b})"
    elif operation == "add":
        boolean_setting = f"({mask_a} OR {mask_b})"
    elif operation == "intersect":
        boolean_setting = f"({mask_a} AND {mask_b})"
    elif operation == "invert":
        boolean_setting = f"(NOT {mask_a})"
    sip.App.GetDocument().ReplaceMaskUsingBooleanExpression(boolean_setting,
                                                            sip.App.GetDocument().GetMaskByName(mask_a),
                                                            sip.App.GetDocument().GetSliceIndices(
                                                                sip.Doc.OrientationYZ),
                                                            sip.Doc.OrientationYZ)
