## Project Process for Version Control in Codesys
1. Edit gitconfig.txt to your repo an your name
2. sometime you have to enable the folder manually

3. run scripts after changes and commit
```mermaid
flowchart TD
    A([Programm Change])
    --> B[Codesys_export.py]
    --> C[git_commitPush.py OR git_commit_push_newbranch.py]
    --> D([Repeat])
```

The Export is for Read-ability and for tracing the changes in code
