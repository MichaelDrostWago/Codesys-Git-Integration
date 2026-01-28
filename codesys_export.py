from __future__ import print_function
from datetime import date
import re, time, os
import xml.dom.minidom as dom
from scriptengine import *  # Import necessary modules

debug = False

today = date.today()

proj=projects.primary
#origProjectFile=proj.export_xml(proj.get_children(True), recursive=True, export_folder_structure=True, declarations_as_plaintext=False)


#newProjectFile=origProjectFile[1:len(origProjectFile)]


### Get Global Project Data ###
project_reference   = projects.primary                         
active_application  = project_reference.active_application      # Get the Active Application
application_name    = active_application.get_name()             # Get Application name
projectpath         = project_reference.path                    # Get Project Location
#project_name        = project_reference.name                    # Get Project Name    
#project_author      = project_reference.author   
#project_company     = project_reference.company 

# Method 2: os.path (handles / and \)
filename = os.path.splitext(os.path.basename(project_reference.path))[0] 
print("Full filename (os):", filename)  


def createDocument(projectpath, project_name):
    """
    creates a file in the project directory
    
    Args:
        filename (str): The name to the file.
        projectpath (str): The Path of the Project.
        project_name (str): The name of the Project.
    """
    ## get Project Path
    delimiter           = projectpath.rfind("\\")                  # find delimiter in path, because absolute path prints also .project ending
    file_ending_size    = len(projectpath) - delimiter - 1
    absolutepath        = projectpath[0:len(projectpath) - file_ending_size]    # Get absolute path without .project ending
    filepath            = absolutepath + "\\" +"_"+project_name+".export"    ##absolutepath + "\\" +"_"+project_name+"_"+str(today)+".export"   
    print(filepath)  
    print(absolutepath)  
    ## Open and Create File
   # f = open(filepath,"w")
    ##f.write("")
    #f.close()
    
    return filepath




print("--- Creating Documentation Files ---")

filePath = createDocument(projectpath, filename)
print("--- at Path: "+filePath+" ---")

#origProjectFile=proj.export_xml(proj.get_children(True), recursive=True,path=filePath, export_folder_structure=True, declarations_as_plaintext=False)
#proj.export_native(filePath, True, profile_name=None, reporter=None)
proj.export_native(
    proj.get_children(True),                    # List[IScriptObject] - MUSS ERSTES!
    filePath,                # str - voller Pfad "C:\\project.export"
    recursive=True,             # Kinder exportieren
    one_file_per_subtree=False, # False=EINE Datei (Git!), True=pro Objekt
    profile_name=None,          # Export-Profil oder None
    reporter=None               # NativeExportReporter oder None
)



#f = open(filePath, "w")
#f.write(origProjectFile)
#f.close()



print("--- Done! ---")