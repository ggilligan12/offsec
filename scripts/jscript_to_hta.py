import sys
import os

def create_hta_from_jscript(jscript_file_path):
    """
    Wraps a JScript file's content in HTML and HTA tags to create a valid HTA script.

    Args:
        jscript_file_path (str): The path to the JScript file.

    Returns:
        str: The content of the JScript file wrapped in HTA tags, or None on error.
    """
    if not os.path.exists(jscript_file_path):
        print(f"Error: JScript file not found at {jscript_file_path}")
        return None

    try:
        with open(jscript_file_path, 'r') as f:
            jscript_content = f.read()
    except Exception as e:
        print(f"Error reading JScript file: {e}")
        return None

    hta_content = f"""<HTML>
<HEAD>
<TITLE>HTA from JScript</TITLE>
<HTA:APPLICATION
     APPLICATIONNAME="HTAFromJScript"
     ID="HTAFromJScript"
     VERSION="1.0"
     SINGLEINSTANCE="yes"
>
</HEAD>
<BODY>
<script language="javascript">
{jscript_content}
</script>
</BODY>
</HTML>
"""
    return hta_content

def write_hta_file(hta_content, jscript_file_path):
    """
    Writes the HTA content to a file with the same name as the JScript file, but with the .hta extension.

    Args:
        hta_content (str): The HTA content to write.
        jscript_file_path (str): The path to the JScript file (used to determine the output file name).

    Returns:
        bool: True on success, False on error.
    """
    hta_file_name = os.path.splitext(jscript_file_path)[0] + ".hta"
    try:
        with open(hta_file_name, 'w') as f:
            f.write(hta_content)
        print(f"HTA file successfully written to {hta_file_name}")
        return True
    except Exception as e:
        print(f"Error writing HTA file: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python jscript_to_hta.py <jscript_file_path>")
        sys.exit(1)

    jscript_file_path = sys.argv[1]
    hta_content = create_hta_from_jscript(jscript_file_path)
    if hta_content:
        write_success = write_hta_file(hta_content, jscript_file_path)
        if not write_success:
            sys.exit(1)  # Exit with an error code if writing failed.
    else:
        sys.exit(1) # Exit with an error code if HTA content creation failed.
