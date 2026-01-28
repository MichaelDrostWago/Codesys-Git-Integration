## Version Control for Codesys Projects

1. Edit gitconfig.txt, this has to be Part of the folder which contains the .project file.
<img width="333" height="110" alt="image" src="https://github.com/user-attachments/assets/c74fa10b-1888-420a-a737-3cb174fda046" />

3. run scripts after changes and commit
```mermaid
flowchart TD
    A([Programm Change])
    --> B[Codesys_export.py]
    --> C[git_commitPush.py OR git_commit_push_newbranch.py]
    --> D([Repeat])
```

The Export is for Read-ability and for tracing the changes in code
<img width="1272" height="514" alt="image" src="https://github.com/user-attachments/assets/9986e1de-65c5-416b-a8f6-3e812f7a0b2b" />


1. Open Script and write commit message
   <img width="429" height="295" alt="image" src="https://github.com/user-attachments/assets/c1198265-c867-434f-afaa-0e43af0eb1c9" />

