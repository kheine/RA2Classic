# $Id: makeEffFromMC_cff.py,v 1.7 2012/12/05 13:10:48 adraeger Exp $
#


import FWCore.ParameterSet.Config as cms
def makeTreeFromPAT(process,
                    outFileName,
                    useCHSJets=True,
		    invertLeptonVeto=False,
                    NJetsMin=2,
                    HTMin=500.,
                    MHTMin=200.,
                    reportEveryEvt=10,
		    Global_Tag="",
		    MCTAP=True,
		    Muon=False,
		    muonTrigger="",
                    testFileName=["/store/user/kheine/HT/RA2PreSelectionOnData_Run2012A_HT_PromptReco-v1_v5/71cce229addb17644d40a607fa20b5d7/RA2SkimsOnData_99_3_TPC.root"],
                    numProcessedEvt=1000):
    
    
    process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
    process.GlobalTag.globaltag = Global_Tag
    
    ## --- Log output ------------------------------------------------------
    process.load("FWCore.MessageService.MessageLogger_cfi")
    process.MessageLogger.cerr = cms.untracked.PSet(
        placeholder = cms.untracked.bool(True)
        )
    process.MessageLogger.statistics.append('cout')
    process.MessageLogger.cout = cms.untracked.PSet(
        INFO = cms.untracked.PSet(reportEvery = cms.untracked.int32(reportEveryEvt))
        )


    ## --- Files to process ------------------------------------------------
    process.maxEvents = cms.untracked.PSet(
        input = cms.untracked.int32(numProcessedEvt)
        )
    process.source = cms.Source(
        "PoolSource",
        fileNames = cms.untracked.vstring(testFileName)
        )
        
        
    ## --- Output file -----------------------------------------------------
    process.TFileService = cms.Service(
        "TFileService",
        fileName = cms.string(outFileName+".root")
        )
    

    ## --- Selection sequences ---------------------------------------------

    # Filter-related selection
    process.load('RA2Classic.TreeMaker.filterSelection_cff')
    process.load('SandBox.Skims.RA2Leptons_cff')

    process.CleaningSelection = cms.Sequence(
        process.filterSelection
        )

    # Filter-related selection
#    process.load('RA2Classic.TreeMaker.filterSelection_cff')
#    from RecoMET.METFilters.jetIDFailureFilter_cfi import jetIDFailure
#    process.PBNRFilter = jetIDFailure.clone(
#        JetSource = cms.InputTag('MHTJets'),
#        MinJetPt      = cms.double(30.0),
#        taggingMode   = cms.bool(False)
#        )
#    process.filterSelection += process.PBNRFilter
#    from RecoMET.METFilters.multiEventFilter_cfi import multiEventFilter
#    process.HCALLaserEvtFilterList2012 = multiEventFilter.clone(
#        file        = cms.FileInPath('EventFilter/HcalRawToDigi/data/AllBadHCALLaser.txt'),
#        taggingMode = cms.bool(False)
#        )
 #   process.filterSelection += process.HCALLaserEvtFilterList2012




    # Produce RA2 jets
    if useCHSJets:
        process.load('RA2Classic.Utils.produceRA2JetsPFCHS_cff')
        process.ProduceRA2Jets = cms.Sequence(
            process.produceRA2JetsPFCHS
            )
    else:
        process.load('RA2Classic.Utils.produceRA2JetsAK5PF_cff')
        process.ProduceRA2Jets = cms.Sequence(
            process.produceRA2JetsAK5PF
            )
	    
	    


    # Select events with at least 'NJetsMin' of the above jets
    from PhysicsTools.PatAlgos.selectionLayer1.jetCountFilter_cfi import countPatJets
    process.NumJetSelection = countPatJets.clone(
        src       = cms.InputTag('HTJets'),
        minNumber = cms.uint32(NJetsMin)
        )

    # HT selection
    htInputCol = 'htPF'
    if useCHSJets:
        htInputCol = 'htPFchs'

    from SandBox.Skims.RA2HT_cff import htPFFilter
    process.HTSelection = htPFFilter.clone(
        HTSource = cms.InputTag(htInputCol),
        MinHT = cms.double(HTMin)
        )

    # MHT selection
    mhtMin = 0.
    mhtInputCol = 'mhtPF'
    if useCHSJets:
        mhtInputCol = 'mhtPFchs'

    from SandBox.Skims.RA2MHT_cff import mhtPFFilter
    process.MHTSelection = mhtPFFilter.clone(
        MHTSource = cms.InputTag(mhtInputCol),
        MinMHT = cms.double(MHTMin)
        )


    ## --- Additional Filters (not tagging mode) ------------------------------
    from RecoMET.METFilters.jetIDFailureFilter_cfi import jetIDFailure
    process.PBNRFilter = jetIDFailure.clone(
        JetSource = cms.InputTag('MHTJets'),
        MinJetPt      = cms.double(30.0),
        taggingMode   = cms.bool(False)
        )
	
	
    from RecoMET.METFilters.multiEventFilter_cfi import multiEventFilter
    process.HCALLaserEvtFilterList2012 = multiEventFilter.clone(
        file        =
        cms.FileInPath('RA2Classic/LostLeptonBkg/data/HCALLaserEventList_20Nov2012-v2_HT-HTMHT.txt'),
        taggingMode = cms.bool(False)
        )
	
	
	
	

    process.AdditionalFiltersInTagMode = cms.Sequence(
        process.PBNRFilter
        )


    ## --- Setup WeightProducer -------------------------------------------
    from RA2Classic.WeightProducer.getWeightProducer_cff import getWeightProducer
    process.WeightProducer = getWeightProducer(process.source.fileNames[0])
        

    ## --- Setup of TreeMaker ----------------------------------------------
    FilterNames = cms.VInputTag()  # All filters in AdditionalFiltersInTagMode
    for f in process.AdditionalFiltersInTagMode.moduleNames():
        FilterNames.append(cms.InputTag(f))

##     FilterNames.append(cms.InputTag("HBHENoiseFilterRA2","HBHENoiseFilterResult","PAT"))
##     FilterNames.append(cms.InputTag("beamHaloFilter"))
##     FilterNames.append(cms.InputTag("eeNoiseFilter"))
##     FilterNames.append(cms.InputTag("trackingFailureFilter"))
##     FilterNames.append(cms.InputTag("inconsistentMuons"))
##     FilterNames.append(cms.InputTag("greedyMuons"))
##     FilterNames.append(cms.InputTag("ra2EcalTPFilter"))
##     FilterNames.append(cms.InputTag("ra2EcalBEFilter"))
##     FilterNames.append(cms.InputTag("hcalLaserEventFilter"))
##     FilterNames.append(cms.InputTag("eeBadScFilter"))

    process.load('Configuration.EventContent.EventContent_cff')
    process.load('Configuration.StandardSequences.MagneticField_38T_cff')
    process.load('Configuration.StandardSequences.Reconstruction_cff')
    process.load('Configuration.StandardSequences.EndOfProcess_cff')
    process.load('Configuration.StandardSequences.GeometryDB_cff')
    process.load('Configuration.StandardSequences.Services_cff')

    process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")





    process.load("MuonAnalysis.MuonAssociators.patMuonsWithTrigger_cff")
    from MuonAnalysis.MuonAssociators.patMuonsWithTrigger_cff import useExistingPATMuons
    useExistingPATMuons(process, "patMuons")

#    process.load("MuonAnalysis.MuonAssociators.patMuonsWithTrigger_cff")

    triggerProcessName = "HLT"
    triggerPathSelector = "HLT_Ele27_WP80_v*"
    matchedCutsString=' path( "'+triggerPathSelector+'",1,0 )'


	
	
	
	# filter used to slecte the RA2 baseline important for efficiency caluclaiton
    from RA2Classic.Utils.RA2Selection_cfi import RA2Selection
    process.RA2Selector = RA2Selection.clone(
    	nJets		= cms.uint32 (1),
	HTMin		= cms.double(50),
	MHTMin		= cms.double(0),
	
	)

   ## ---- Load lost lepton moduels
   # special calo jets for delta R in efficiencies
    process.load('JetMETCorrections.Configuration.DefaultJEC_cff')

   

    from RA2Classic.LostLeptonBkg.promtisomu_cfi import promtIsoMu
    process.promtLeptons = promtIsoMu.clone(
	MuonIDISOTag = cms.InputTag("patMuonsPFIDIso"),
	CaloJetTag = cms.InputTag("ak5CaloJetsL2L3"),
#	CaloJetTag	= cms.InputTag('cleanPatJetsAK5Calo'),
    )
    from RA2Classic.LostLeptonBkg.tapTreeProducer_cfi import tapTreeProducer
    process.tapTreeMuId = tapTreeProducer.clone(
	HTTag	   = cms.InputTag(htInputCol),
 	MHTTag	   = cms.InputTag(mhtInputCol),
	MC	   = cms.bool(MCTAP),
	Muon	   = True,
	MuonTrigger     =cms.string(muonTrigger),
	
    )
    process.tapTreeMuIso = process.tapTreeMuId.clone(
       MuElecIdIso    = cms.uint32(1),
       Muon	      = True
    )
    process.tapTreeElecId = process.tapTreeMuId.clone(
       MuElecIdIso    = cms.uint32(2),
       Muon	      = False
    )
    process.tapTreeElecIso = process.tapTreeMuId.clone(
       MuElecIdIso    = cms.uint32(3),
       Muon	      = False
    )
    process.tapTreeElecIdGsf = process.tapTreeMuId.clone(
       MuElecIdIso    = cms.uint32(4),
       Muon	      = False
    )
    


 #electrons selectors for ID electrons
    from SandBox.Skims.RA2Leptons_cff import patElectronsID
    from SandBox.Skims.RA2Leptons_cff import patElectronsIDIso
    process.ra2ElectronsID = patElectronsID.clone()
    process.ra2ElectronsIDIso = patElectronsIDIso.clone()
 
 
 # JES variation for MET 
    from RA2Classic.Utils.jesUncertaintyVariation_cfi import jesUncertaintyVariation
    process.jesUp = jesUncertaintyVariation.clone(
        Jets       = cms.InputTag('MHTJets'), # The input jet collection
        JetTypeId  = cms.string('AK5PFchs'),  # Type of the input jets (to obtain the uncertainty from the data base). 
        Variation  = cms.string('Up')         # Either 'Up' or 'Dn' to produce jets with JES +/- 1 sigma, respectively
    )
    process.jesDown = jesUncertaintyVariation.clone(
        Jets       = cms.InputTag('MHTJets'), # The input jet collection
        JetTypeId  = cms.string('AK5PFchs'),  # Type of the input jets (to obtain the uncertainty from the data base). 
        Variation  = cms.string('Down')         # Either 'Up' or 'Dn' to produce jets with JES +/- 1 sigma, respectively
    )



    process.tapProducer = cms.Sequence ()
    if Muon :
	    process.tapProducer+=process.patMuonsWithTriggerSequence
	    process.tapProducer+=process.tapTreeMuId
	    process.tapProducer+=process.tapTreeMuIso
    else :
	    process.tapProducer+=process.patMuonsWithTriggerSequence
	    process.tapProducer+=process.tapTreeElecIdGsf
	    process.tapProducer+=process.tapTreeElecIso
    if MCTAP  :
	    process.tapProducer+=process.tapTreeMuId
	    process.tapProducer+=process.tapTreeMuIso
	    process.tapProducer+=process.tapTreeElecIdGsf
	    process.tapProducer+=process.tapTreeElecIso


    ## --- Final paths ----------------------------------------------------

    process.dump = cms.EDAnalyzer("EventContentAnalyzer")
    
    process.WriteTree = cms.Path(
        process.CleaningSelection *
	process.HCALLaserEvtFilterList2012 *
	process.ProduceRA2Jets *
        process.NumJetSelection *
        process.HTSelection *
        process.MHTSelection *
        process.AdditionalFiltersInTagMode *
        process.WeightProducer *
	process.ra2ElectronsID *
	process.ra2ElectronsIDIso *
#	process.jesUp *
#	process.jesDown *
#	process.promtLeptons *
	process.RA2Selector *
#	process.ak5CaloJetsL2L3 *
    	process.tapProducer 
#	process.dump *
#	process.patMuonsWithTriggerSequence *
#	process.LostLeptonBkgMCEffCalculator *
#	process.LostLeptonBkgProducer
#	process.RA2TreeMaker 

        )
