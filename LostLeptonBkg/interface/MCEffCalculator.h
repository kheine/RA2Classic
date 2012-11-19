#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/Provenance/interface/EventAuxiliary.h"
#include "FWCore/Utilities/interface/EDMException.h"


#include <DataFormats/PatCandidates/interface/Jet.h>
#include <DataFormats/PatCandidates/interface/MET.h>
#include <DataFormats/PatCandidates/interface/Muon.h>
#include <DataFormats/PatCandidates/interface/Electron.h>
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Common/interface/View.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "TH2.h"
#include <utility>
#include <vector>
#include "TString.h"
#include "TTree.h"

#include "DataFormats/Candidate/interface/CandMatchMap.h"





//
// class declaration
//

class MCEffCalculator : public edm::EDAnalyzer {
   public:
      explicit MCEffCalculator(const edm::ParameterSet&);
      ~MCEffCalculator();
	// first deltaR second CloestJetPT
	static std::pair <double,double> DRToClosestJet(const edm::Event& iEvent, edm::InputTag caloJetTag_, double lepEta, double lepPhi);
	static double MTWCalculator(const edm::Event& iEvent, edm::InputTag MTTag, double lepPT, double lepPhi);

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);


   private:
      virtual void beginJob() ;
      virtual void analyze(const edm::Event&, const edm::EventSetup&);
      virtual void endJob() ;

      virtual void beginRun(edm::Run const&, edm::EventSetup const&);
      virtual void endRun(edm::Run const&, edm::EventSetup const&);
      virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&);
      virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&);

	//special functions
	void MuonFound(reco::GenParticleCollection::const_iterator cand, unsigned int i);
	void ElecFound(reco::GenParticleCollection::const_iterator cand, unsigned int i);
	void TauFound(const reco::Candidate* tau);
	void ResetValues();

	//Tags
  	edm::InputTag evtWeightTag_;
  	edm::InputTag muonIDTag_, muonIDISOTag_;
  	edm::InputTag elecIDTag_, elecIDISOTag_;

	edm::InputTag caloJetTag_;
  	edm::InputTag metTag_;
  	edm::InputTag genTag_;
	
	// additional input tags for plotting
	edm::InputTag HtJetsTag_, MhtJetsTag_, HTTag_,MHTTag_, NVTag_;
   	edm::InputTag muonPromtMatchedTag_;


      // Variables
	//Input
	double minMuonPt_, minElecPt_, minJetPt_, maxMuonEta_, maxElecEta_;
	float eventWeight_;
	unsigned int nGenMu_, nGenElec_;
	TH2F *muonIDPassedTH2F_, *muonIsoPassedTH2F_, *muonIsoPassedUpTH2F_, *muonIsoPassedDownTH2F_;
	TH2F *muonIDPassed2TH2F_, *muonIsoPassed2TH2F_, *muonIsoPassedUp2TH2F_, *muonIsoPassedDown2TH2F_;

	TH2F *elecIDPassedTH2F_, *elecIsoPassedTH2F_, *elecIsoPassedUpTH2F_, *elecIsoPassedDownTH2F_;
	TH2F *elecIDPassed2TH2F_, *elecIsoPassed2TH2F_, *elecIsoPassedUp2TH2F_, *elecIsoPassedDown2TH2F_;

 	TH2F *muonIDFailedTH2F_, *muonIsoFailedTH2F_, *muonIsoFailedUpTH2F_, *muonIsoFailedDownTH2F_;
 	TH2F *muonIDFailed2TH2F_, *muonIsoFailed2TH2F_, *muonIsoFailedUp2TH2F_, *muonIsoFailedDown2TH2F_;

	TH2F *elecIDFailedTH2F_, *elecIsoFailedTH2F_, *elecIsoFailedUpTH2F_, *elecIsoFailedDownTH2F_;
	TH2F *elecIDFailed2TH2F_, *elecIsoFailed2TH2F_, *elecIsoFailedUp2TH2F_, *elecIsoFailedDown2TH2F_;

	TH2F *MuonMTPassedTH2F_, *MuonMTFailedTH2F_;

	TH1F *MuonAccPassedTH1F_, *MuonAccFailedTH1F_;
	TH1F *MuonAccPassed2TH1F_, *MuonAccFailed2TH1F_;
	TH1F *ElecAccPassedTH1F_, *ElecAccFailedTH1F_;
	TH1F *ElecAccPassed2TH1F_, *ElecAccFailed2TH1F_;

	TH2F *MTWTH2F_;


	//Tree and stuff to be filed in it
        TString treeName_;
        TTree* tree_;

	int muonNumberRecoID_, elecNumberRecoID_, leptons_;
	Float_t muonPTAccPassed_, elecPTAccPassed_;
	double muonIDPassed_, muonIDFailed_, elecIDPassed_, elecIDFailed_, muonRecoPt_, muonRecoEta_, muonRecoPhi_, elecRecoPt_, elecRecoEta_, elecRecoPhi_;
	Float_t muonGenPt_, muonGenEta_, muonGenPhi_, elecGenPt_, elecGenEta_, elecGenPhi_;
	Float_t deltaGenR_, closestJetToMuonGenPt_,closestJetToElecGenPt_, mt_, mtw_, mtwElec_;
	// reco iso eff plots
	TH2F *elecIdEffTH2F_, *elecIsoEffTH2F_, *elecIsoEffUpTH2F_, *elecIsoEffDownTH2F_;
 	TH2F *muonIdEffTH2F_, *muonIsoEffTH2F_, *muonIsoEffUpTH2F_, *muonIsoEffDownTH2F_;	


	//Varialbes used for studies
	Float_t RecoMuonDeltaR_, RecoMuonPTJet_, RecoMuonPTRelJet_, IsoMuonDeltaR_, IsoMuonPTJet_, IsoMuonPTRelJet_, RecoGenMuDeltaR_;
	// changed for now to Float_t since the plotting tool cant handel any int
	int nRecoMu_, nRecoElec_, nIsoMu_, nIsoElec_, nAccMu_, nAccElec_;
	//not plotted
	Float_t muonIsoPt_, muonIsoEta_, muonIsoPhi_;

	Float_t RecoElecDeltaR_, RecoElecPTJet_, RecoElecPTRelJet_, IsoElecDeltaR_, IsoElecPTJet_, IsoElecPTRelJet_, RecoGenElecDeltaR_;
	//not plotted
	Float_t elecIsoPt_, elecIsoEta_, elecIsoPhi_;

	// only for plotting purposes
	Float_t ht_, mht_;
	UShort_t nJets_, nV_;
	int isExpectation_;
	int nMuInIsoMuCollection_;
	int muPromtMatched_;

	// testing
	int ntau_, ntauMu_, ntauElec_;
};