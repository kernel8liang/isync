# isync

A tool used to easy distributed development, sync your git based project to your distributed development machines.

## why this tool?

when each time after make, I need go into each machine sync the modification manually, this is really bother me. And also easy to make misstake, forget sync or do with wrong command. There are some solutions can do this, like Rsync+sersync, it is too heavy, and config is too complex, not flexible enough. docker can do this too, but is too heavy too, when i just modify one .cc which reflect to modify a .so in runtime, it will push the file sytem, in each remote macine to pull the images, shutdown the container, start the image.
I don't like these ways. I need a light, clean, fast way, so write these script.

## how it works?

the principle is simple. use git to control the deploy, every time you make a modification，use git to record which file has been modified. ssh to the remote machines, pull these changes.

there three steps to do so.

1, save the origin .git file in your project to ./origin_back, when your project inblude other projects as submodule, .git in the submodule will be save to ./origin_back_submoduleName recursively, this is done by paser the .gitmodules file recursively. Then move deploy .git into the project root directory, and fllow "git add", "git push";

2, ssh to remote machine, do the git pull.

3, after depoly switch the origin .git file saved in step1 and the depolyed .git.


## how to use it?

clone this repo, put it anywhere you want, add it in your PATH.

note: you need setup ssh key access before use this tool, which shoud be done with other tool or manually.

fisrt time to use it, you shoud to run ```is_config``` command, it will help you to set enviroment variables.

>```DEFAULT_USER```:  the user name you used in your distributed machines, it shoud be same over the cluster. <br>
>```DEFAULT_WORKSPACE```: the directory which contain your projects. <br>
>```DEFAULT_PROJECT_NAME```: the project name. <br>
>```DEFAULT_HOSTS_FILE```: list the machine's ip you want to sync. <br>
>```DEFAULT_IP```: ip address you working on, other machines will pull source code from this ip. <br>

any of these variables can be covered from "is" command parameters.


>```is [-w worksapce] [-n projectName] [-h hostsfile] [-i ip_address] [-u user] [-r]``` <br>
>```-w``` specify your workspace,<br>
>```-n``` specify your project name,<br>
>```-h``` specify your hosts file,<br>
>```-i``` specify your ip,<br>
>```-u``` spccify your name,<br>
>```-r``` if use this parameter, it will clean remote machine's repo and clone a new one.<br>


for example you can ```is -n myproject``` to sync different project "myproject" in the workspace which is not same as the default one.
