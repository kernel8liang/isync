import os
import sys


if __name__ == '__main__':

    bashfile = sys.argv[1]
    homedir = sys.argv[2]


    env_varibles = {
                    "DEFAULT_WORKSPACE": ("%s/workspace") % (homedir),
                    "DEFAULT_PROJECT_NAME":"isync",
                    "DEFAULT_IP":"10.214.129.14",
                    "DEFAULT_USER":"deepinsight",
                    "DEFAULT_HOSTS_FILE": ("%s/workspace/.hosts") % (homedir)
                    }

    for ev in env_varibles:
        print ev
        print "default : ", env_varibles[ev]
        line = sys.stdin.readline()
        line = line.strip()
        if not line:
            continue
        env_varibles[ev] = line


    config_lines = []

    for ev in env_varibles:
        config_lines.append(("export %s=%s") % (ev, env_varibles[ev]))


    print "your config:"
    for line in config_lines:
        print line

    print "do you confirm your setting? / default yes (yes/no) ?"
    line = sys.stdin.readline()
    line = line.strip()
    if not line or line == "yes":
        pass
    else:
        exit -1

    f = open(bashfile)
    bash_lines = []
    for line in f:
        find = False
        for ev in env_varibles:
            ret = line.find(("%s=") % (ev))
            if ret != -1:
                find = True
                break

        if find:
            continue
        bash_lines.append(line)

    f.close()

    for line in config_lines:
        bash_lines.append(("%s\n") % (line))

    wf = open(bashfile, "w")
    for line in bash_lines:
        wf.write(line)

    wf.flush()
    wf.close()

