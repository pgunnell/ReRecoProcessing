#
# eval `scramv1 runtime -csh`
# # set CRAB environment
# source  /afs/cern.ch/cms/ccs/wm/scripts/Crab/crab.sh
# voms-proxy-init

from prepare_conf import prepare

#check GT but seems good in autoCond

prepare(era="Run2018A",
        proc_string="ForValUL2018",
        GT="106X_dataRun2_v20")

prepare(era="Run2018B",
        proc_string="ForValUL2018",
        GT="106X_dataRun2_v20")

prepare(era="Run2018C",
        proc_string="ForValUL2018",
        GT="106X_dataRun2_v20")

prepare(era="Run2018D",
        proc_string="ForValUL2018",
        GT="106X_dataRun2_v20")

