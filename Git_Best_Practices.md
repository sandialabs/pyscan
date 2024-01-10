# Best Practices for Using Git With Our Repository

## 1. Cloning the Github Repository

To clone the GitHub repository you must have first installed git to your machine.


Next, navigate to the GitHub page and click on the green <> Code button drop down menu. Then copy the HTTPS URL.


Open a terminal (gitbash, anaconda, or equivalent) and type the following command (replace the copied URL if different):
`git clone https://github.com/sandialabs/pyscan.git`


Now you can simply follow the README installation guide if you want to make use of the program; however,
if you want to edit the program in any way it is best to create a new branch so that your changes can be saved as separate 
from the main pyscan application and shared as a unique adaptation of the original program.


## Important Note:

All the following git commands are to be submitted in the terminal (gitbash, anaconda, or equivalent). We recommend anaconda.


## 2. Branches

### 2.1 Getting an Existing Remote Branch from GitHub:

To see all branches that exist on GitHub and on your local machine use the command:
`git branch -a`

To get and switch to a remote branch use the command:
`git checkout remote-branch-name-here`

In response the terminal should say: `branch 'remote-branch-name-here' set up to track 'origin/remote-branch-name-here'`.
If so, you will now be on that remote branch. 
Otherwise, you may have created a new, strictly local branch on accident. Make sure you typed the remote branch name correctly and try again.


### 2.2 Creating and Switching to a New Branch

To create a new branch, type the following command followed by the name of your branch (this will not switch to the branch and remain on the active branch until you switch as described in the following steps):
`git branch my-branch-name-here`

(The style for the branch name should follow this syntax, with each word separated by a hyphen.)

If you want to see a list of the branches currently exist on your local machine, type the following command:
`git branch`

(To delete unnecessary or accidental branches you can use the command: `git branch -d branch-name-to-delete`)

Now you can switch to the branch you just made (or switch to a pre-existing branch) using the following command with the corresponding branch name:
`git switch branch-name-I-want-to-switch-to`

Now any saves that you make will be saved to your current branch and no longer affect other branches. 

### 2.3 Committing Changes to your Branch

If you want to know which branch you are currently on you can type the following command:
`git status`
This will also show if you have saved changes you have not committed to git. 

Each time you commit to git it will save the current state of your branch.
This is more useful than simply saving your work because you can return to each commit later, in case you want to revert to a previous state of your branch.

To commit changes to all the files you have been working on use the following command:
`git commit -am "And leave a note here summarizing the changes you made to this commit here to have a log for keeping track. This will be useful later."`

Alternatively, you can commit the changes you made to individual files by using the following command with the path to the file you are committing:
`git commit -m "Note your changes here." path/to/my/file.ext`

You may notice that if you create new files, git will not automatically add them to your commits. To add them to git so that they will be tracked with each commit use the command:
`git add path/to/my/file.ext`

### 2.4 Resetting Your Branch to the Repositories Current State

If you want to undo changes to your branch and simply reset to the original state, you can reset your branch to the repositories current state.

Before doing this it is recommended you save your work to a new branch by first committing your work (i.e. `git commit -am "Saving my work, just in case"`) and then creating a new branch (i.e. `git branch my-saved-work`). This way you won't lose anything because you can still access your current state (before resetting) on this new branch later.

Once your work is saved, you can reset to the remote branch's state using the commands:
`git fetch origin`
`git reset --hard origin/branch-name`


############## Talk about git stash here before or in replacement of the following reset instructions since it seems like a safer option? ###########################

### 2.5 Resetting your Branch to a Previous Commit
############## I think we should include this because this is best practice rather than using revert, but what do you think? #########

#### THIS CAN BE DANGEROUS AS YOU CAN LOSE A LOT OF YOUR WORK, so DO THIS AT YOUR OWN RISK!
###
Furthermore, only do this on your local machine, do not try this on our repository! Instead, if you want a commit reverted on the GitHub repository please submit an issues request for us to handle.

It is HIGHLY recommended you back up your current state to another branch or directory first.
To save your current branches state first you can first commit (i.e. `git commit -am "Saving my work, just in case"`),
then create a new branch (i.e. `git branch my-saved-work`), that way you can still access your work on this new branch later.

To reset you must first locate the hash of the commit you want to return to. 
The hash will be the 40 character hexadecimal string of numbers and letters, which will look something like this: `8159595fbf3f16ce7184008d14e9df7c9eb04f5f`
There are several ways to find this.

To see a history of changes made and their corresponding hashes you can use the command: `git log`; however, to make use of this it is important to have made good notes for your past commits so that you can accurately identify which one you wish to return to.

You may also find commit hashes for commits to the repository on GitHub by first going to the branch you are working with, clicking on the Commits (just under the green <> Code button), and copying the hash of the commit you want to return to. Once you are SURE you have copied the correct hash you can reset your current progress to that corresponding commit with the command:
`git reset hash-here`

Now your state will be reset to the commit corresponding to the hash, and all intermediary commits will be deleted.


## 3. Sharing, Updating, and Managing Your Branch in Relation to the GitHub Repository

### 3.1 Sharing
If you want to share your branch by adding it to the GitHub repository you must first log in to a GitHub account. 
Then you can share your branch to the repository with the following command (though you may need to request permission from us first): `git push`; however, if your branch is not up to date with changes made to the same branch on the GitHub repository you will encounter an error message.

### 3.2 Merging and Pulling

To fix this you will need to fetch the changes to update your current view of the main repository and then merge those changes with your branch to proceed. This can be accomplished by using `git fetch` followed by `git merge origin branch-name` or, more simply, `git pull` which is a combination of git fetch and merge. Using git pull will pull changes made to your current branch from the repository, or alternatively you can select a different branch to pull changes from (i.e. `git pull origin main`) which will pull changes from the selected origin branch to your current local branch.

You can also merge your local branches using `git merge branch-name`, which will additively combine branches.

Upon attempting to merge YOU MAY NEED TO RESOLVE CONFLICTS between your branch and the branch you are pulling from.
If you see a CONFLICT message, you will need to address merge conflicts in the files listed. (If you are unsure whether there was a conflict or whether a conflict was resolved, using `git status` will show whether ther are unmerged paths after attempting to merge.)
If there is a conflict and you don't want to resolve it you can abort the merge at this stage and return to your branches state before the pull/merge using the command:
`git merge --abort`

### 3.3 Resolving Conflicts

To to resolve conflicts first go through each of the files listed to find the conflicts (there may be more than one instance!). Once in the files, the conflicts will be bracketed in the code with the following syntax:

<<<<<<< HEAD
Current state of your local branch that is in conflict with the incoming merge
=======
Current state of the branch you are merging from that is in conflict with your current branch
>>>>>>>

To resolve this in Microsoft Visual Studio Code (which we recommend) you will be presented with options above the conflict to:
    1. Accept Current Change (to keep the version you have in your current branch)
    2. Accept Incoming Change (to keep the version you have in the branch you are merging with)
    3. Accept Both Changes (changes will be added consecutively in the order they appear within the conflict brackets)
    4. Compare Changes (to visualize the differences between each version)

If you are not in Visual Studio Code you can manually resolve conflicts by replacing the conflict notations (both brackets and it's contents) with what you want to remain.
For example, the manually resolved conflict from the conflict listed above (starting with <<<<<<< HEAD) you could keep both the current state of your branch AND the current state of the branch you are merging from by deleting the brackets and separating equal signs:

`Current state of your local branch that is in conflict with the incoming merge`
`Current state of the branch you are merging from that is in conflict with your current branch`

Otherwise, only keep the state you want to finalize and delete everything you don't want included. For example, if you want to implement the incoming change (from the branch you are pulling/merging from) over and instead of your current state, all that would remain of the manually edited conflict is:

`Current state of the branch you are merging from that is in conflict with your current branch`

Once you have resolved the conflict(s) you must commit the changes, using the aforementioned commands (i.e. `git commit -am "Note what branch you merged and other changes here."`).

Now if you use `git status` it should show that there are no changes to update.

Finally, you may use `git push` to share your now up to date branch with the world, adding it to our repository.


## 4. Pull Requests

At some point you may wish to add your changes to the main, or another branch on our GitHub repository to benefit other's ability to make use of this pyscan program. We welcome your requests; however, we ask that you only make a pull request once your branch has been tested using our provided pytest test cases and is shown to be fully functional. 

You may see if your branch passes our test cases using GitHub once you have pushed your branches changes to the repository. Simply navigate to the Actions tab on the GitHub webpage, select `Python application` under Actions on the left, and then run your workflow using the `Run workflow` button and selecting your branch.

This will help us to stay on top of updating pyscan meaningfully as different pull requests come in.

To submit a pull request navigate to the pull requests tab on our GitHub page. Then click to create a pull request. First select the base branch you want to merge to, then select the branch you want to merge from. Please include a meaningful note detailing why you want to merge these two branches to help us evaluate your request.


## 5. Issues With Pyscan

If you find a bug with any of our branches we welcome and encourage you to report it through the issues tab on our GitHub page. Simply navigate to the branch you found issue with, go to the issues tab, and submit a report describing the problem you identified. We will work to address and resolve this issue once we receive your request. 

Thank you for your help in improving and maintaining pyscan!
    