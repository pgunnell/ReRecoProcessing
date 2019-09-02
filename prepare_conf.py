#
# eval `scramv1 runtime -csh`
# # set CRAB environment
# source  /afs/cern.ch/cms/ccs/wm/scripts/Crab/crab.sh
# voms-proxy-init

import os
import  sys,time,json
from    dbs.apis.dbsClient import DbsApi
from    time import gmtime
import commands
url="https://cmsweb.cern.ch/dbs/prod/global/DBSReader"
api=DbsApi(url=url)

from Configuration.Skimming.autoSkim import autoSkim
#from autoSkim import autoSkim

#print autoSkim

from Configuration.AlCa.autoAlca import AlCaRecoMatrix
# USING LOCAL autoAlca.py
#from autoAlca import autoAlca

#print autoAlca

#========================================================
# TOP level configuration goes here
# NOTE: you need to edit the cmsDriver commands below directly in the code

#
# acquisition_era = "Run2016D"
#
# GT = "80X_dataRun2_2016SeptRepro_v3"
# proc_string = "23Sep2016"
#
def prepare(era, proc_string, GT):

    


    acquisition_era = era
#    if("Run2016B" in era):
#        acquisition_era = "Run2016B"

    customera = {}
    customera["Run2018A"] = 'Configuration/DataProcessing/RecoTLR.customisePostEra_Run2_2018'
    customera["Run2018B"] = 'Configuration/DataProcessing/RecoTLR.customisePostEra_Run2_2018'
    customera["Run2018C"] = 'Configuration/DataProcessing/RecoTLR.customisePostEra_Run2_2018'
    customera["Run2018D"] = 'Configuration/DataProcessing/RecoTLR.customisePostEra_Run2_2018'

    jsonFile = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/DCSOnly/json_DCSONLY.txt'

    default_priority = 110100

    pd_blacklist = ["HighMultiplicity",
                    "HLTPhysics", #FIXME should be?
                    "HcalNZS",
                    "HcalHPDNoise",
                    "Commissioning",
                    "Cosmics",
                    "EmptyBX",
                    'ExpressAlignment',
                    'AlCaPhiSym',
                    'L1Accept',
                    'JetHT-Error',
                    'MET-Error',
                    'AlCaLumiPixels',
                    'AlCaP0',
                    'RPCMonitor',
                    'TestEnablesEcalHcal',
                    'DoubleEG-Error',
#                    'IsolatedBunch',
                    'IsolatedBunch-Error',
                    'Pixel5',
# The following datasets have no events
                    'HighPtPhoton30AndZ',
                    'HighPtLowerPhotons',
                    'DoubleMuonLowMass'
                    ]
    # for ds in api.listDatasets(dataset='/HIN*/%s*/RAW' % acquisition_era):
    #     pd_blacklist.append(ds['dataset'].split('/')[1])
    #
    for ds in api.listDatasets(dataset='/L1MinimumBias*/%s*/RAW' % acquisition_era):
        pd_blacklist.append(ds['dataset'].split('/')[1])
        
    for ds in api.listDatasets(dataset='/Ephemeral*/%s*/RAW' % acquisition_era):
        pd_blacklist.append(ds['dataset'].split('/')[1])
        
    for ds in api.listDatasets(dataset='/ZeroBias*/%s*/RAW' % acquisition_era):
        pd_tmp = ds['dataset'].split('/')[1]
        if(pd_tmp != 'ZeroBias'):
            pd_blacklist.append(pd_tmp)

    for ds in api.listDatasets(dataset='/Parking*/%s*/RAW' % acquisition_era):
        pd_tmp = ds['dataset'].split('/')[1]
        pd_blacklist.append(pd_tmp)

    for ds in api.listDatasets(dataset='/HLTPhysics*/%s*/RAW' % acquisition_era):
        pd_tmp = ds['dataset'].split('/')[1]
        pd_blacklist.append(pd_tmp)

    for ds in api.listDatasets(dataset='/Scouting*/%s*/RAW' % acquisition_era):
        pd_tmp = ds['dataset'].split('/')[1]
        pd_blacklist.append(pd_tmp)

    for ds in api.listDatasets(dataset='/HI*/%s*/RAW' % acquisition_era):
        pd_tmp = ds['dataset'].split('/')[1]
        pd_blacklist.append(pd_tmp)

    print 'list of blacklisted PDs:'
    print pd_blacklist
    # FIXME: add mapping of priority for PD which need higher-priority
    # JEC: ZeroBias/SinglePhoton/JetHT/DoubleEG/DoubleMu

    pd_priorities = {}
    # these are the PDs for JME
   # pd_priorities['NoBPTX'] = 87000
   # pd_priorities['SingleElectron'] = 93500
   # pd_priorities['MET'] = 93500
   # pd_priorities['SingleMuon'] = 93500
   # pd_priorities['Charmonium'] = 87000
   # pd_priorities['MuonEG'] = 93500
   # pd_priorities['JetHT'] = 93500
   # pd_priorities['MuOnia'] = 87000
   # pd_priorities['HeavyFlavor'] = 87000
   # pd_priorities['FSQJet2'] = 87000
   # pd_priorities['FSQJet1'] = 87000



    campaign = 'UltraLegacy2018'
    num_core = 8

    # if (era == 'Run2016B-v2') :
    #     proc_string = proc_string+'_ver2'
    # if (era == 'Run2016B-v1') :
    #     proc_string = proc_string+'_ver1'

    # =======================================================
    # Here we get some variables from the environment
    username = os.environ['USER']
    cmssw_version = os.environ['CMSSW_VERSION']
    print 'USER: %s' % username
    print 'CMSSW_VERSION: %s' % cmssw_version

    # ======================================================

    with open(jsonFile) as data_file:
        data = json.load(data_file)
    # print data.keys()
    AlltheRuns = map(int,data.keys())
    print sorted(AlltheRuns)
    print "# of runs in the JSON: ", len(AlltheRuns)
    # select runs up to which we want to reprocess
    
    #one could use also a map for that (mapping era and runs)
    if (acquisition_era=='Run2018A'):
        theRuns = filter(lambda x: (x == 315420), AlltheRuns)

    elif (acquisition_era=='Run2018B'):
        theRuns = filter(lambda x: (x in [317626, 317640, 317641, 317182]), AlltheRuns)

    elif (acquisition_era=='Run2018C'):
        theRuns = filter(lambda x: (x == 320065), AlltheRuns)

    elif (acquisition_era=='Run2018D'):
        theRuns = filter(lambda x: (x in [324021, 324022, 324077, 325101]), AlltheRuns)
    
    else:
        theRuns = 0
    #theRuns = AlltheRuns
    print sorted(theRuns)

#    theDatasets = api.listDatasets(data_tier_name='RAW', acquisition_era_name='%s' % era)
#    theDatasets = api.listDatasets(data_tier_name='RAW', processed_ds_name='*%s*' % era)
    theDatasets = api.listDatasets( dataset='/*/%s*/RAW' % era )

    print theDatasets

    # theDatasetsAOD = api.listDatasets( data_tier_name='AOD', acquisition_era_name='Run2016B')
#    theDatasetsAOD = api.listDatasets(data_tier_name='AOD', processed_ds_name='*%s*' % acquisition_era)
    theDatasetsAOD = api.listDatasets( dataset='/*/*%s*/AOD' % acquisition_era)
    if len(theDatasetsAOD):
        # most likely this run is still not done in prompt...we assume that all datasets are
        theDatasetsAOD = theDatasets

    print '# of RAW datasets matching era %s: %i' % (acquisition_era, len(theDatasets))
    # print theDatasets
    print '# of AOD datasets matching era %s: %i' % (acquisition_era, len(theDatasetsAOD))
    # print theDatasetsAOD
    theDatasetsToProcessAOD = []
    theDatasetsToProcess = []

    for mydataset in theDatasetsAOD:
        tempdataset = mydataset['dataset']
        theDatasetsToProcessAOD.append((tempdataset.split('/'))[1])

    print '# of PDs having AOD dataset in prompt %i' % len(theDatasetsToProcessAOD)
    #NOTE: this is NOT the # of PDs since here there is multiplicity due to various prompt reco version making each PD to appear n times
    #print theDatasetsToProcessAOD

    if not os.path.exists(era):
        os.makedirs(era)
    previous_dir = os.getcwd()
    os.chdir(era)

    nd = 0
    twiki=file('twiki_%s.twiki' % campaign, 'w')
    twiki.write('---+++ !%s \n\n' % acquisition_era)
    twiki.write('| *DataSet* | *prepID monitoring* | *run* |\n')


#    master=file('master_'+era+'.conf','w')
#    master.write("[DEFAULT] \n")
#    master.write("group=ppd \n")
#    master.write("user=%s \n" % username)
#    master.write("request_type=ReReco \n")
#    master.write("release=%s \n" % cmssw_version)
#    master.write("globaltag=%s \n" % GT)
#    master.write("\n")
#    master.write("campaign="+campaign+"\n")
#    master.write("acquisition_era="+acquisition_era+"\n")

#    master.write("\n")
#    master.write("processing_string="+proc_string+" \n")
#    master.write("\n")
#    master.write("priority=%i \n" % default_priority)
#    if ("SingleMuon" in pd_name):
#        master.write("time_event=3.2 \n")
#        master.write("size_event=874 \n")
#    elif ("ZeroBias" in pd_name):
#        master.write("time_event= \n")
#        master.write("size_event= \n")
#    elif ("SingleElectron" in pd_name):
#        master.write("time_event= \n")
#        master.write("size_event= \n")
#    elif ("JetHT" in pd_name):
#        master.write("time_event= \n")
#        master.write("size_event= \n")
#    elif ("DoubleMuon" in pd_name):
#        master.write("time_event= \n")
#        master.write("size_event= \n")
#    elif ("DoubleEG" in pd_name):
#        master.write("time_event= \n")
#        master.write("size_event= \n")
#    elif ("SinglePhoton" in pd_name):
#        master.write("time_event= \n")
#        master.write("size_event= \n")
#    master.write("size_memory = 14000 \n")
#    master.write("multicore=%i \n" % num_core)

#    cfg_harvesting_file_name = 'harvesting.py'
#    master.write("harvest_cfg=%s \n" % cfg_harvesting_file_name)

#    harvesting_command = 'cmsDriver.py step4 --data --filetype DQM --conditions %s -s HARVESTING:@rerecoZeroBias --era Run2_2017 --scenario pp --filein file:RECO_RAW2DIGI_L1Reco_RECO_ALCA_EI_PAT_DQM_inDQM.root --python_filename=%s --no_exec' % (GT, cfg_harvesting_file_name)
#    if not os.path.isfile(cfg_harvesting_file_name):
#        print 'creating harvesting cfg...'
#        st_and_out_harvst = commands.getstatusoutput(harvesting_command)
#        if st_and_out_harvst[0] != 0:
#            print '[ERROR] cfg creation failed with message: %s' % st_and_out_harvst[1]



#    master.flush()

    for oneDS in theDatasets:

        theDataset= oneDS['dataset']
        pd_name = theDataset.split('/')[1]
        era_version = theDataset.split('/')[2]


        print '--- dataset %s' % theDataset
        print '--- era %s' % era_version

        if pd_name in theDatasetsToProcessAOD:
            if pd_name in pd_blacklist:
                print '    PD is blacklisted'
                continue

            print '    adding to re-reco matrix'

            if not("ZeroBias" in pd_name or "JetHT" in pd_name or "SingleMuon" in pd_name or "DoubleMuon" in pd_name or "EGamma" in pd_name or "MET" in pd_name):
                continue

            #print oneDS
            #print api.listRuns(dataset=theDataset)
            runs = api.listRuns(dataset=theDataset)[0]['run_num']

            if("NoBPTX" in (pd_name) ):
                inter = set(runs)
            else:
                inter = set(runs) & set(theRuns)
                
            if len(inter) > 0 :
                theDatasetsToProcess.append(theDataset)

                nd = nd+1
                theruns = sorted(inter)

                cfg_file_name = 'recoskim_%s_%s.py' % (era, pd_name)
                prep_id = "ReReco-"+acquisition_era+"-"+pd_name+"-"+proc_string+"-"+(format(nd, '04d'))
                #print cfg_file_name
                # Now write the section of the cfg specific to this PD/request
                master=file('master_'+era+'_'+pd_name+'.conf','w')
                master.write("[DEFAULT] \n")
                master.write("group=ppd \n")
                master.write("user=%s \n" % username)
                master.write("request_type=ReReco \n")
                master.write("release=%s \n" % cmssw_version)
                master.write("globaltag=%s \n" % GT)
                master.write("\n")
                master.write("campaign="+campaign+"\n")
                master.write("acquisition_era="+acquisition_era+"\n")
                
                master.write("\n")
                master.write("processing_string="+proc_string+" \n")
                master.write("\n")
                master.write("priority=%i \n" % default_priority)

                if ("SingleMuon" in pd_name):
                    master.write("time_event=3.2 \n")
                    master.write("size_event=874 \n")
                elif ("ZeroBias" in pd_name):
                    master.write("time_event=1.6 \n")
                    master.write("size_event=1405 \n")
                elif ("MET" in pd_name):
                    master.write("time_event=1.9 \n")
                    master.write("size_event=566 \n")
                elif ("JetHT" in pd_name):
                    master.write("time_event= 1.7 \n")
                    master.write("size_event= 1455 \n")
                elif ("DoubleMuon" in pd_name):
                    master.write("time_event= 1.5 \n")
                    master.write("size_event= 451 \n")
                elif ("EGamma" in pd_name):
                    master.write("time_event=3.1 \n")
                    master.write("size_event=1811 \n")
              
                master.write("size_memory = 14000 \n")
                master.write("multicore=%i \n" % num_core)    
                master.write("\n")
                master.write('[%s-%s-%s]\n' % (era_version, pd_name, proc_string))
                master.write("dset_run_dict={\""+theDataset+"\" : "+str(theruns)+" }\n")
                master.write("cfg_path=%s\n" % cfg_file_name)
                master.write("request_id=%s \n" % prep_id)
                # here create the cfg file

                alcaseq = ''
                skimseq = ''
                recotier = ''
                dqmseq = ''
                keepreco = False

    #            if ( ("NoBPTX" in pd_name) or ("DoubleMuon" in pd_name) or ("EmptyBX" in pd_name) or
    #            ("ZeroBias" in pd_name) or ("MinimumBias" in pd_name) or ("SingleMu" in pd_name) ) :
    #                keepreco = True
    #                recotier = 'RECO,'
#                if ("NoBPTX" in pd_name) :
#                recotier = 'RECO,'

#                if ("ZeroBias" in pd_name) :
#                    alcaseq = 'ALCA:SiStripCalZeroBias+TkAlMinBias+LumiPixelsMinBias+SiStripCalMinBias+AlCaPCCZeroBiasFromRECO,'
                

#                if pd_name in pd_priorities.keys():
#                    master.write("priority=%i \n" % pd_priorities[pd_name])

#                if pd_name in autoSkim.keys():
#                    skimseq='SKIM:%s,'%(autoSkim[pd_name])

#NEED TO CHECK THE SKIM

                if ("ZeroBias" in pd_name or "DoubleMuon" in pd_name or "SingleElectron" in pd_name) :
                    skimseq = ''
                elif ("JetHT" in pd_name) :
                    skimseq = 'SKIM:JetHTJetPlusHOFilter,'
                elif ("DoubleEG" in pd_name):
                    skimseq = 'SKIM:ZElectron+EXOMONOPOLE,'
                elif ("SingleMuon" in pd_name):    
                    skimseq = 'SKIM:MuonPOGSkim+ZMu+MuTau,'
                elif ("SinglePhoton" in pd_name):
                    skimseq = 'SKIM:SinglePhotonJetPlusHOFilter+EXOMONOPOLE,'

                if pd_name in AlCaRecoMatrix.keys():
                    alcaseq='ALCA:%s,'%(AlCaRecoMatrix[pd_name])

                if ("ZeroBias" in pd_name) :
                    dqmseq = 'DQM:@rerecoZeroBias'
                elif ("SingleMuon" in pd_name) :
                    dqmseq = 'DQM:@rerecoSingleMuon'
                else : 
                    dqmseq = 'DQM:@rerecoCommon'
    


                # if ( (pd_name in autoSkim.keys()) and (not(keepreco)) ) :
                #    #            if ( (pd_name_short in autoSkim.keys()) and (not(keepreco)) ) :
                #    master.write("transient_output = [\"RECOoutput\"]")
                #    master.write("\n")
                #    recotier='RECO,'

                input_file_name = 'file:test.root'
                if ("ZeroBias" in pd_name) :
                    reco_command = 'cmsDriver.py RECO -s RAW2DIGI,L1Reco,RECO,%sEI,PAT,%s --runUnscheduled --nThreads %i --data --era Run2_2018 --scenario pp --conditions %s --customise_commands="process.DQMStore.saveByLumi = cms.untracked.bool(True)"  --eventcontent %sAOD,MINIAOD,DQM --datatier %sAOD,MINIAOD,DQMIO --customise %s,Configuration/DataProcessing/Utils.addMonitoring --filein %s -n 100 --python_filename=%s --no_exec' % (skimseq+alcaseq, dqmseq, num_core, GT, recotier, recotier, str(customera[acquisition_era]), input_file_name, cfg_file_name)
                else:
                    reco_command = 'cmsDriver.py RECO -s RAW2DIGI,L1Reco,RECO,%sEI,PAT,%s --runUnscheduled --nThreads %i --data --era Run2_2018 --scenario pp --conditions %s  --customise_commands="process.DQMStore.saveByLumi = cms.untracked.bool(True)" --eventcontent %sAOD,MINIAOD,DQM --datatier %sAOD,MINIAOD,DQMIO --customise %s,Configuration/DataProcessing/Utils.addMonitoring --filein %s -n 100 --python_filename=%s --no_exec' % (skimseq+alcaseq, dqmseq, num_core,GT, recotier, recotier, str(customera[acquisition_era]), input_file_name, cfg_file_name)

#                reco_command = 'cmsDriver.py RECO -s RAW2DIGI,L1Reco,RECO,%sEI,PAT,DQM:@allForPrompt --runUnscheduled --nThreads %i --data --era Run2_2016 --scenario pp --conditions %s --eventcontent %sAOD,MINIAOD,DQM --datatier %sAOD,MINIAOD,DQMIO --customise %s --filein %s -n 100 --python_filename=%s --no_exec' % (skimseq+alcaseq, num_core, GT, recotier, recotier, customera[campaign], input_file_name, cfg_file_name)
                print '    cmsDriver command: %s' % reco_command

                if not os.path.isfile(cfg_file_name):
                    print '     creating the cfg...'
                    st_and_out = commands.getstatusoutput(reco_command)
                    if st_and_out[0] != 0:
                        print '[ERROR] cfg creation failed with message: %s' % st_and_out[1]

                print ' creating harvesting...'        


                harvseq=''       

                if ("ZeroBias" in pd_name) :
                    harvseq = '@rerecoZeroBias'
                elif ("SingleMuon" in pd_name) :
                    harvseq = '@rerecoSingleMuon'
                else :
                    harvseq = '@rerecoCommon'

                cfg_harvesting_file_name = 'harvesting_%s_%s.py'  % (era, pd_name)
                master.write("harvest_cfg=%s \n" % cfg_harvesting_file_name)
                

                List_for_harvest = ['ZeroBias','JetHT','SingleMuon','EGamma']

                cust_harvest = False

                for element in List_for_harvest:
                    if (element in pd_name) :
                        cust_harvest = True

                if(cust_harvest):
                    harvesting_command = 'cmsDriver.py step4 --data --filetype DQM --conditions %s -s HARVESTING:%s --customise_commands="process.DQMStore.saveByLumi = cms.untracked.bool(True)" --era Run2_2018 --scenario pp --filein file:RECO_RAW2DIGI_L1Reco_RECO_ALCA_EI_PAT_DQM_inDQM.root --python_filename=%s --no_exec' % (GT, harvseq, cfg_harvesting_file_name)

                else :
                    harvesting_command = 'cmsDriver.py step4 --data --filetype DQM --conditions %s -s HARVESTING:%s --era Run2_2018 --scenario pp --filein file:RECO_RAW2DIGI_L1Reco_RECO_ALCA_EI_PAT_DQM_inDQM.root --python_filename=%s --no_exec' % (GT, harvseq, cfg_harvesting_file_name)
                        
                print '    cmsDriver command: %s' % harvesting_command

                if not os.path.isfile(cfg_harvesting_file_name):
                    print 'creating harvesting cfg...'
                    st_and_out_harvst = commands.getstatusoutput(harvesting_command)
                    if st_and_out_harvst[0] != 0:
                        print '[ERROR] cfg creation failed with message: %s' % st_and_out_harvst[1]
                

                master.flush()
                twiki.write("| %s | [[https://cms-pdmv.cern.ch/pmp/historical?r=%s][%s]] | %s |\n"  %(theDataset, prep_id, prep_id, str(theruns)))
                master.close()

            else:
                print '    [WARNING] dataset has no runs in DCS JSON, skipping'

        else:
            print '    no AOD for this in prompt-reco: skipping'

    ################################

    ##### printout for twiki
    #            print "|"+theDataset+"|"+str(theruns)+"|"
    ################################
    os.chdir(previous_dir)
    twiki.close()

    print
    print
    #print theDatasetsToProcess
    print "\n".join(theDatasetsToProcess)
    print "number of datasets with run overlap: %s"%(len(theDatasetsToProcess))
    print "number of datasets with AOD: %s"%(len(theDatasetsToProcessAOD))
