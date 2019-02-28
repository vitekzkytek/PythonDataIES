# Quick set-up of Jupyter and GitHub


## Launching Jupyter from the GitHub
0) Install latest [Anaconda](https://www.anaconda.com/download/) and [GitHub](https://gist.github.com/derhuerst/1b15ff4652a867391f03) on your computer. You should also create your GitHub account.

1) On the main page of [Fork](https://guides.github.com/activities/forking/) this repository to your account. Copy the link to your version of the repository (for example using `Clone or download` button)
2) Launch the command shell ([Windows](https://www.digitalcitizen.life/7-ways-launch-command-prompt-windows-7-windows-8) or [Mac](https://macpaw.com/how-to/use-terminal-on-mac))
3) Using `cd` find the directory that you want to save your repository into. I.e. if you want your repository saved directly in the `Documents` folder go into `Documents` folder.
4) Type `git clone [link]` (without brackets).
Hurray, you downloaded your very first GitHub repo
5) Go to your git directory, i.e. type `cd [projectName]`
6) Type `jupyter notebook` in your command shell.
Your Jupyter should be running on [localhost:8888](http:\\localhost:8888)


## Pushing your changes on the GitHub server.
Whenever you do changes on your computer, it is only stored on the computer. It will not propagate into the GitHub repository.

This part assumets that your shell command is set inside your project directory. 
In order to *push* changes online, you will need to do the following:
1) Pull the last version of the repository using `git pull origin [branch]`
You need to this only if you are not sure that the only difference between version stored in the GitHub's branch and the one you have on your local computer are the ones that you have made since your last [pull] or [clone] request.

If neither you nor anyone else did not make any changes to the code, anywhere else  (including direct editations your GitHub account! ), the pull request is not necessary.

2) Using `git add *` you will *stage* the changes that you made 
3) Using  `git commit -m "commit description"` command you will commit the staged changes with description `commit description`.
4) Using `git push origin [branch]` you will propagate your changes to the GitHub account.

