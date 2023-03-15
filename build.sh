if ! command -v buildah &> /dev/null
then
    echo "buildah not installed, check docker"
    if ! command -v docker &> /dev/null
    then
        echo "Not buildah neither docker is installed. Exit"
        return 1 2>/dev/null
    else
        echo "using docker"
        builder="docker"
        build_command="$builder build --file $1 -t $2 ."
    fi
else
    echo "using buildah"
    builder="buildah"
    build_command="$builder bud -f $1 -t $2"
fi
echo "--- Building $2 from configuration $1"
$build_command
echo "--- Pushing $2"
$builder push $2