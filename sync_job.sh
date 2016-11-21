workspace=$1
reclone=$2
project_name=$3
ip=$4
user=$5

if [ ! -d $workspace ]; then
    mkdir -p $workspace
fi

if [ $reclone == true ]; then
    echo "rm workspace to reclone it."
    echo rm -rf $workspace/$project_name
    rm -rf $workspace/$project_name
fi

if [ ! -d $workspace/$project_name ]; then
    cd $workspace
    git clone ssh://$user@$ip/$workspace/$project_name
else
    cd $workspace/$project_name
    git pull ssh://$user@$ip/$workspace/$project_name
fi

