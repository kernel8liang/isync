import sys
import os
import Magic

if __name__  == '__main__':

    if len(sys.argv) != 3:
        print "wrong number of args, except 3"
        exit(-1)

    print "revert ..."

    workspace_base = sys.argv[1]
    project_name = sys.argv[2]

    #first move deploy's .git to deploy backup direactroy.

    depoly_current_backup = ("%s/%s_%s") % (workspace_base, Magic.Magic.magic_deploy,project_name)
    project_root = ("%s/%s") % (workspace_base, project_name)
    depoly_current_git = ("%s/.git*") % (project_root)

    cmd = ("mv %s %s") % (depoly_current_git, depoly_current_backup)
    os.system(cmd)

    store_file =("%s/%s/store_info") % (workspace_base, Magic.Magic.magic_orign)
    f = open(store_file)

    for line in f:
        line = line.split()
        git_files = ("%s/.git*") % (line[1])
        cmd = ("mv %s %s") % (git_files, line[0])
        os.system(cmd)

    #clean store_file
    origin_back =("%s/%s/*") % (workspace_base, Magic.Magic.magic_orign)
    cmd = ("rm -rf %s") % (origin_back)
    os.system(cmd)
