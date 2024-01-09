Cloning the Github Repository

    To clone the GitHub repository you must have first installed git to your machine.


    Next, navigate to the GitHub page and click on the green <> Code button drop down menu. Then copy the HTTPS URL.


    Open a terminal (gitbash, anaconda, or equivalent) and type the following command followed by the URL:
    git clone Copied-URL-Here

    it should look something like this:
    git clone https://github.com/sandialabs/pyscan.git


    Now you can simply follow the README installation guide if you want to make use of the program; however,
    if you want to edit the program in any way it is best to create a new branch so that your changes can be saved as separate 
    from the main pyscan application and shared as a unique adaptation of the original program.


Important Note:

    All the following git commands are to be submitted in the terminal (gitbash, anaconda, or equivalent). We recommend anaconda.


Getting an Existing Remote Branch from GitHub:

    To see all branches that exist on GitHub and on your local machine use the command:
    git branch -a

    To get and switch to a remote branch use the command:
    git checkout remote-branch-name-here

    It should say "branch 'remote-branch-name-here' set up to track 'origin/remote-branch-name-here'". If so, you will now be on that remote branch. 
    Otherwise, make sure you typed the remote branch name correctly and try again.


Creating and Managing Branches

    To create a new branch, type the following command followed by the name of your branch (this will not switch to the branch and remain on the active branch until you switch as described in the following steps):
    git branch my-branch-name-here

    (The style for the branch name should follow this syntax, with each word separated by a hyphen.)

    If you want to see a list of the branches currently exist on your local machine, type the following command:
    git branch

    (To delete unnecessary or accidental branches you can use the command: git branch -d branch-name-to-delete)

    Now you can switch to the branch you just made (or switch to a pre-existing branch) using the following command with the corresponding branch name:
    git switch branch-name-I-want-to-switch-to

    Now any saves that you make will be saved to your current branch. If you want to know which branch you are currently on you can type the following command:
    git status

    This will also show if you have saved changes you have not committed to git. Each time you commit to git it will save the current state of your branch.
    This is more useful than simply saving your work because you can return to each commit later, in case you want to revert to a previous state of your branch.
    To commit changes to all the files you have been working on use the following command:
    git commit -am "And leave a note about what changes you made here to have a log for keeping track of the main changes you made to this commit."

    Alternatively, you can commit the changes you made to individual files by using the following command with the path to the file you are committing:
    git commit -m "Note your changes here." path/to/my/file.ext

    To see a full history of changes made using git you can use the command:
    git log

    You may notice that if you create new files, git will not automatically commit them. To add them to git so that they will be tracked with each commit use the command:
    git add path/to/my/file.ext

    ############## I think we should include this because this is best practice rather than using revert, but what do you think? #########
    If you wish to undo your current changes and return to a previous state, there is a way to do this; however, THIS CAN BE DANGEROUS AS YOU CAN LOSE A LOT OF YOUR CODE, so DO THIS AT YOUR OWN RISK!
    Furthermore, only do this on your local machine, do not try this on our repository! Instead, if you want a commit reverted on the GitHub repository please submit an issues request for us to handle.
    It is recommended to back up your current state to another branch or directory first. To save your current branches state first you can first commit (i.e. git commit -am "Saving my work, just in case"),
    then create a new branch (i.e. git branch my-saved-work), that way you won't lose any of your 
    
    To reset you must first locate the hash of the commit you want to return to. There are several ways to do this.
    The first and most simple is by using git log; however, to make use of this it is important to have made good notes for your past commits so that you can identify the one you wish to return to. 
    The hash will be the 40 character hexadecimal string of numbers and letters, which will look something like this: 8159595fbf3f16ce7184008d14e9df7c9eb04f5f.
    You may also find commit hashes on GitHub by first going to the branch you are working with, clicking on the Commits (just under the green <> Code button), and 
    copying the hash of the commit you want to return to. Once you are SURE you have copied the correct hash you can reset your current progress to that corresponding commit with the command:
    git reset hash-here

    Another alternative for resetting your current state to a remote branches state is to use the commands:
    git fetch origin
    git reset --hard origin/branch-name

    Again, it is a good idea to save your current branches state first using:
    git commit -am "Saving my work, just in case"
    git branch my-saved-work


Sharing, Updating, and Managing Your Branch in Relation to the GitHub Repository

    If you want to share your branch by adding it to the GitHub repository you must first log in to a GitHub account. 
    Then you can with the following command (though you may need to request permission from us first):
    git push
    
    However, if your branch is not up to date with changes made to the same branch on the GitHub repository you will encounter an error message.
    To fix this you will need to fetch the changes to update your current view of the main repository and then merge those changes with your branch to proceed.

    You can fetch the current status of the repository using the command:  git fetch   to help keep track of these changes.
    When you are ready to sync your branch with the repository branch you can merge branches with the original repository branch using the following command:
    git merge origin branch-name

    (You can also merge a different local branch with your current branch by using: git merge branch-you-want-to-merge-with)

    Or if you want to fetch and merge with the original repository branch at the same time you can use:
    git pull

    Upon attempting to merge YOU MAY NEED TO RESOLVE CONFLICTS between your branch and the repository branch.
    If you see a CONFLICT message, you will need to manually address merge conflicts in the files listed.
    If you are unsure whether there was a conflict or whether a conflict was resolved, using:  git status   will show whether ther are unmerged paths. To abort the merge at this stage 


    To do so go through each of the files listed to find the conflicts (there may be more than one instance!), which will be bracketed and separated in the following syntax:

    <<<<<<< HEAD
    Current state of your local branch that is in conflict with the incoming merge
    =======
    Current state of the branch you are merging from that is in conflict with your current branch
    >>>>>>>

    To resolve this in Microsoft Visual Studio Code (which we recommend) you will be presented with options above the HEAD to:
        1. Accept Current Change (to keep the version you have in your current branch)
        2. Accept Incoming Change (to keep the version you have in the branch you are merging with)
        3. Accept Both Changes (changes will be added consecutively in the order they appear within the conflict brackets)
        4. Compare Changes (to visualize the differences between each version)

    If you are not in Visual Studio Code you can manually resolve conflicts by replacing the conflict notations (both brackets and it's contents) with what you want to remain.
    For example, the manually resolved conflict from the above conflict could look something like:

    Current state of your local branch that is in conflict with the incoming merge
    Current state of the branch you are merging from that is in conflict with your current branch

    If you want to keep both the current state of your branch AND the current state of the branch you are merging from.

    Once you have resolved the conflict(s) you must commit the changes, using the aforementioned commands (i.e. git commit -am "Note what branch you merged and other changes here.")

    Now if you use git status it should show that there are no changes to update.


Pull Requests

    At some point you may wish to add your changes to the main, or another branch on our GitHub repository to benefit others ability to make use of this pyscan program.
    We welcome your requests; however, we ask that you use them sparingly, intentionally, and only for significant improvements to the functionality.
    This will help us to stay on top of updating pyscan meaningfully as different pull requests come in.

    To submit a pull request navigate to the pull requests tab on our GitHub page. Then click to create a pull request and select the base branch you want to merge to 
    and the branch you want to merge from to the base branch. Please leave a meaningful note detailing why you want to merge this two branches to help us evaluate your request.


Issues With Pyscan

    If you find a bug with any of our branches we welcome and encourage you to report it through the issues tab on our GitHub page.
    Simply navigate to the branch you found issue with, go to the issues tab, and submit a report describing the problem you identified.
    We will work to address and resolve this issue once we receive your request. Thank you for your help in improving and maintaining pyscan!
    