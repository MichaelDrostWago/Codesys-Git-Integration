# encoding:utf-8
from __future__ import print_function
from datetime import date
import re, time, os
import subprocess
import sys

# === USER SETTINGS =====================================================
REMOTE_NAME = "origin"
BRANCH_NAME = "main"
FOLDER_TO_COMMIT = "."  # "." = whole project
# =======================================================================

project_reference   = projects.primary                         
projectpath         = project_reference.path                    

print(project_reference)
print(projectpath)

filename = os.path.splitext(os.path.basename(project_reference.path))[0] 
print("Full Filename (os):", filename)  

print("Commit Message")
commitMessage = system.ui.query_string("Commit Message")

# === PARSE gitconfig.txt (URL + USER) ==================================
def parse_gitconfig(repo_path):
    """Parse gitconfig.txt for URL, name, email."""
    config_path = os.path.join(repo_path, "gitconfig.txt")
    
    if not os.path.isfile(config_path):
        print("gitconfig.txt not found - using fallback")
        return GITEA_REPO_URL, "Michael", "michael.drost@mail.de"
    
    try:
        with open(config_path, "r") as f:
            content = f.read()
        
        print("gitconfig.txt preview:")
        print(repr(content[:300]))
        
        # URL: Handle your malformed [remote 'origin'] [url]
        url_match = re.search(r'\[remote\s*["\']?origin["\']?\]?\s*\[?([^\]\n]+(?:http[^}\]]+)[^\]\n]*)\]?', content, re.IGNORECASE)
        repo_url = url_match.group(1).strip() if url_match else " "
        
        # User name
        name_match = re.search(r'\[user\]\s*\n\s*name\s*=\s*([^\n]+)', content, re.IGNORECASE | re.MULTILINE)
        user_name = name_match.group(1).strip() if name_match else " "
        
        # User email
        email_match = re.search(r'\[user\]\s*\n\s*email\s*=\s*([^\n]+)', content, re.IGNORECASE | re.MULTILINE)
        user_email = email_match.group(1).strip() if email_match else " "
        
        print("✓ Parsed - URL:", repo_url)
        print("✓ Parsed - Name:", user_name)
        print("✓ Parsed - Email:", user_email)
        
        return repo_url, user_name, user_email
        
    except Exception as e:
        print("gitconfig.txt error:", str(e))
        return "none", "none", "none"

# === GIT HELPER ========================================================
def run_git(args, cwd=None):
    cmd_str = " ".join(["git"] + [str(a) for a in args])
    print("Running:", cmd_str)
    
    try:
        output = subprocess.check_output(cmd_str, shell=True, cwd=cwd, stderr=subprocess.STDOUT)
        print("  ✓", output.strip())
        return True
    except subprocess.CalledProcessError as e:
        print("  ✗ (code %d):" % e.returncode, e.output.strip())
        return False
    except Exception as e:
        print("  ✗", str(e))
        return False

# === MAIN ==============================================================
if commitMessage and commitMessage.strip():
    repo_path = os.path.dirname(projectpath)
    repo_path = os.path.abspath(repo_path)
    
    print("Repo path:", repo_path)
    
    # *** PARSE gitconfig.txt FOR URL+USER ***
    ACTUAL_REPO_URL, USER_NAME, USER_EMAIL = parse_gitconfig(repo_path)
    # *** END ***
    
    # Init Git repo
    if not os.path.isdir(os.path.join(repo_path, ".git")):
        run_git(["init"], repo_path)
    
    # Set parsed user config
    run_git(["config", "user.name", USER_NAME], repo_path)
    run_git(["config", "user.email", USER_EMAIL], repo_path)
    
    # Setup remote from config
    run_git(["remote", "remove", REMOTE_NAME], repo_path)
    run_git(["remote", "add", REMOTE_NAME, ACTUAL_REPO_URL], repo_path)
    
    folder_abs = os.path.join(repo_path, FOLDER_TO_COMMIT.replace("\\", "/"))
    print("Committing:", folder_abs)
    
    # Add → Commit → Push
    if run_git(["add", "-A", FOLDER_TO_COMMIT], repo_path):
        if run_git(["commit", "-m", commitMessage], repo_path):
            print("✓ COMMITTED!")
            run_git(["branch", "-M", BRANCH_NAME], repo_path)
            if run_git(["push", "-u", REMOTE_NAME, BRANCH_NAME], repo_path):
                print("🎉 PUSHED!")
            else:
                print("✗ Push failed - manual git push first?")
        else:
            print("✗ Nothing to commit")
    else:
        print("✗ Staging failed")
else:
    print("Cancelled.")
