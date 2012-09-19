import FWCore.ParameterSet.Config as cms

process = cms.Process("Trigger")

###############################################################################
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.threshold = 'INFO'
process.MessageLogger.cerr.FwkReport.reportEvery = 100
###############################################################################

## Options and Output Report
process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32( 1000 ) )

process.source = cms.Source("PoolSource",
   fileNames = cms.untracked.vstring(
    '/store/user/kheine/HT/RA2PreSelectionOnData_Run2012A_HT_PromptReco-v1_v7/e99cf838fe40ef4081c91a81748e6000/RA2SkimsOnData_312_1_l4U.root',
    '/store/user/kheine/HT/RA2PreSelectionOnData_Run2012A_HT_PromptReco-v1_v7/e99cf838fe40ef4081c91a81748e6000/RA2SkimsOnData_290_1_Iru.root',
    '/store/user/kheine/HT/RA2PreSelectionOnData_Run2012A_HT_PromptReco-v1_v7/e99cf838fe40ef4081c91a81748e6000/RA2SkimsOnData_212_1_LUQ.root',
    '/store/user/kheine/HT/RA2PreSelectionOnData_Run2012A_HT_PromptReco-v1_v7/e99cf838fe40ef4081c91a81748e6000/RA2SkimsOnData_90_1_XTv.root',
    '/store/user/kheine/HT/RA2PreSelectionOnData_Run2012A_HT_PromptReco-v1_v7/e99cf838fe40ef4081c91a81748e6000/RA2SkimsOnData_465_1_TUf.root',
    '/store/user/kheine/HT/RA2PreSelectionOnData_Run2012A_HT_PromptReco-v1_v7/e99cf838fe40ef4081c91a81748e6000/RA2SkimsOnData_448_1_Isw.root',
    '/store/user/kheine/HT/RA2PreSelectionOnData_Run2012A_HT_PromptReco-v1_v7/e99cf838fe40ef4081c91a81748e6000/RA2SkimsOnData_38_1_FlO.root',
    '/store/user/kheine/HT/RA2PreSelectionOnData_Run2012A_HT_PromptReco-v1_v7/e99cf838fe40ef4081c91a81748e6000/RA2SkimsOnData_496_1_omW.root',               
    )
)
###############################################################################
## Global tags and geometry
# default configuration with frontier conditions
process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = cms.string('GR_R_52_V9D::All')
###############################################################################

###############################################################################
process.TFileService = cms.Service("TFileService",fileName = cms.string("Trigger_2012.root") )
###############################################################################
process.load("RA2Classic.Trigger.trigger_cfi")
process.trigger.jet_pt_cut_MHT = 30.
process.trigger.jet_pt_cut_HT = 50.
#process.trigger.jetCollection = 'patJetsPF'
process.trigger.jetCollection = 'patJetsAK5PF'
###############################################################################

###############################################################################
process.load("SandBox.Skims.filterBoolean_cfi")
process.RA2_HBHENoiseFilterRA2    = process.booleanFilter.clone()
process.RA2_HBHENoiseFilterRA2.ResultSource = cms.InputTag("HBHENoiseFilterRA2","HBHENoiseFilterResult","PAT")
process.RA2_beamHaloFilter        = process.booleanFilter.clone()
process.RA2_beamHaloFilter.ResultSource = cms.InputTag("beamHaloFilter")
process.RA2_eeNoiseFilter         = process.booleanFilter.clone()
process.RA2_eeNoiseFilter.ResultSource = cms.InputTag("eeNoiseFilter")
process.RA2_trackingFailureFilter = process.booleanFilter.clone()
process.RA2_trackingFailureFilter.ResultSource = cms.InputTag("trackingFailureFilter")
process.RA2_inconsistentMuons     = process.booleanFilter.clone()
process.RA2_inconsistentMuons.ResultSource = cms.InputTag("inconsistentMuons")
process.RA2_greedyMuons           = process.booleanFilter.clone()
process.RA2_greedyMuons.ResultSource = cms.InputTag("greedyMuons")
process.RA2_EcalTPFilter          = process.booleanFilter.clone()
process.RA2_EcalTPFilter.ResultSource = cms.InputTag("ra2EcalTPFilter")
process.RA2_EcalBEFilter          = process.booleanFilter.clone()
process.RA2_EcalBEFilter.ResultSource = cms.InputTag("ra2EcalBEFilter")
process.HcalLaserEventFilter      = process.booleanFilter.clone()
process.HcalLaserEventFilter.ResultSource = cms.InputTag("hcalLaserEventFilter")
process.EEBadScFilter             = process.booleanFilter.clone()
process.EEBadScFilter.ResultSource = cms.InputTag("eeBadScFilter")
###############################################################################

###############################################################################
process.load('SandBox.Skims.RA2HT_cff')
###############################################################################

process.dump = cms.EDAnalyzer("EventContentAnalyzer")

process.turnon = cms.Path(
   # process.dump*
    process.htPFFilter *    # to be used for standard jets
    #process.htPFchsFilter *  # to be used for chs jets
    process.RA2_HBHENoiseFilterRA2 *
    process.RA2_beamHaloFilter *
    process.RA2_eeNoiseFilter *
    process.RA2_trackingFailureFilter *
    process.RA2_inconsistentMuons *
    process.RA2_greedyMuons *
    process.RA2_EcalTPFilter *
    process.RA2_EcalBEFilter *
    process.HcalLaserEventFilter *
    process.EEBadScFilter *
    process.trigger
    )

