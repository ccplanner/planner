if [ -z "$FAST_DOWNWARD_HOME" ]; then
    echo "FAST_DOWNWARD_HOME not set";
    exit -1
fi
    
if [ -z "$2" ]; then
    echo "usage: fd_run.sh <domain pddl file> <problem pddl file>";
    exit -1
fi

cp $1 $FAST_DOWNWARD_HOME/src/tmp-domain.pddl
cp $2 $FAST_DOWNWARD_HOME/src/tmp-problem.pddl
cd $FAST_DOWNWARD_HOME/src
rm output*
rm sas_plan
translate/translate.py tmp-domain.pddl tmp-problem.pddl
preprocess/preprocess < output.sas
search/downward --search "astar(blind())" < output
echo ""
echo "The plan:"
cat sas_plan | tr ')' ' ' | cut -d ' ' -f 5 | sed 's/dir-//g'
cd -
