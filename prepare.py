import sys
import os

class Magic:
    '''magic for back dircetory'''
    magic_orign = ".ababc234back_origin"
    magic_deploy = ".ababc234back_deploy"


def paser_gitmodule(gitmodule_file):

    f = open(gitmodule_file)
    modules = []
    #used to check 0, 1, 0, 1 sequence
    pair_open = False

    project_name = None
    project_path = None
    for line in f:
        line = line.strip()
        #check very carefuly because this is a basic tools
        if line[0] == "[" and line[-1] == "]":
            line = line[1 : -1]
            tokens = line.split()
            if len(tokens) == 2:
                first = tokens[0].strip()
                if  first == "submodule":
                    if pair_open != False:
                        return False, modules
                    #maybe put submodule with diff name and some other path
                    #so split tokes[1] again, and take the last part as the name of
                    #the submodule
                    tokens = tokens[1].split("/")
                    project_name = tokens[-1].strip()
                    project_name = project_name.strip('"')
                    pair_open = True
        else:
            tokens = line.split("=")
            if len(tokens) == 2:
                first = tokens[0].strip()
                if first == "path":
                    if pair_open != True:
                        return False, modules
                    project_path = tokens[1].strip()
                    pair_open = False
                    #a pair has beed check correct put is into modules
                    modules.append((project_name, project_path))

    return True, modules

def save_origin_git_recursive(workspace_base, project_root, project_name):

    #check the .gitmodules file is exist
    gitmodule_file = ("%s/%s") % (project_root, ".gitmodules")
    ret = os.path.isfile(gitmodule_file)

    if ret:
        success, modules = paser_gitmodule(gitmodule_file)
        if not success:
            print ("%s has something wrong!") % (project_root)
            return False

        for module in modules:
            #module --- [project_name, project_path]
            next_project_root = ("%s/%s") % (project_root, module[1])
            success = save_origin_git_recursive(workspace_base, next_project_root, module[0])
            if not success:
                return False

    #copy all the current level .git* to .ababc234back_origin
    current_level_git = ("%s/%s") % (project_root, ".git")
    back_current_origin = ("%s/%s/%s") % (workspace_base, Magic.magic_orign, project_name)

    #store project_root and corrsponding back directory here
    store_file = ("%s/%s/store_info") % (workspace_base, Magic.magic_orign)
    f = open(store_file, "a")
    f.write(("%s %s\n") % (project_root, back_current_origin))
    f.flush()
    f.close()

    #if current is a git project back all .git to the back_current_origin
    ret = os.path.exists(current_level_git)
    if not ret:
        print "project don't have .git ignore"
    else:
        current_level_git = ("%s/%s") % (project_root, ".git*")
        if not os.path.exists(back_current_origin):
            os.mkdir(back_current_origin)
        cmd = ("mv %s %s") % (current_level_git, back_current_origin)
        os.system(cmd)

    return True

if __name__ == '__main__':

    if len(sys.argv) != 3:
        print "wrong number of args, except 3"
        exit(-1)

    print "prepare ..."

    workspace_base = sys.argv[1]
    project_name = sys.argv[2]

    ret = os.path.exists(workspace_base)
    if not ret:
        print "your workspace is not exists", workspace_base
        exit(-1)

    project_path = ("%s/%s") % (workspace_base, project_name)
    ret = os.path.exists(project_path)

    if not ret:
        print "your porject is not exists", project_path
        exit(-1)


    back_origin = ("%s/%s") % (workspace_base, Magic.magic_orign)
    ret = os.path.exists(back_origin)
    if not ret:
        os.mkdir(back_origin)

    #back_origin_root = ("%s/%s") % (workspace_base, Magic.magic)
    project_root = ("%s/%s") % (workspace_base, project_name)

    success = save_origin_git_recursive(workspace_base, project_root, project_name)
    if not success:
        exit(-1)

    #switch deploy .git into work space
    depoly_current = ("%s/%s_%s") % (workspace_base, Magic.magic_deploy, project_name)
    #first time depoly need create direactory.
    ret = os.path.exists(depoly_current)
    if not ret:
        print "first time to depoly ", project_name, "may spent a little time"
        os.mkdir(depoly_current)
        cmd = ("cd  %s; git init .; git add .; git commit -m 'for deploy';") % (project_root)
        os.system(cmd);
    else:
        cmd = ("mv %s/.git* %s; cd %s; git add .; git commit -m'for deploy'") % (depoly_current, project_root, project_root)
        #cmd = ("mv %s/.git* %s;") % (depoly_current, project_root)
        os.system(cmd);

