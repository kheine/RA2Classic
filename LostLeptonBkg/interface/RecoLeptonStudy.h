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
#include "TH3.h"
#include <utility>
#include <vector>
#include "TString.h"
#include "TTree.h"

#include "DataFormats/Candidate/interface/CandMatchMap.h"
#include "TLorentzVector.h"
#include <DataFormats/JetReco/interface/CaloJet.h>




//
// class declaration
//

class RecoLeptonStudy : public edm::EDAnalyzer {
   public:
      explicit RecoLeptonStudy(const edm::ParameterSet&);
      ~RecoLeptonStudy();
	// first deltaR second CloestJetPT
	static std::pair <double,double> DRToClosestJet(const edm::Event& iEvent, edm::InputTag caloJetTag_, double lepEta, double lepPhi);
	static double MTWCalculator(const edm::Event& iEvent, edm::InputTag MTTag, double lepPT, double lepPhi);

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);
	edm::View <reco::Candidate>::const_iterator LeptonMatch(const edm::View <reco::Candidate>  &MuID, Float_t lepGenEta, Float_t lepGenPhi, Float_t lepGenPt);


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
	bool Z_;


      // Variables
	//Input
	double minMuonPt_, minElecPt_, minJetPt_, maxMuonEta_, maxElecEta_;
	float eventWeight_;
	unsigned int nGenMu_, nGenElec_;
	bool debug_;



	//Tree and stuff to be filed in it
        TString treeName_;
        TTree* tree_;

	int muonNumberRecoID_, elecNumberRecoID_, leptons_, tauFound_;
	Float_t muonPTAccPassed_, elecPTAccPassed_;
	// changed to float_t!! from double 12 12 2012
	Float_t muonIDPassed_, muonIDFailed_, elecIDPassed_, elecIDFailed_, muonRecoPt_, muonRecoEta_, muonRecoPhi_, elecRecoPt_, elecRecoEta_, elecRecoPhi_;
	Float_t muonGenPt_, muonGenEta_, muonGenPhi_, elecGenPt_, elecGenEta_, elecGenPhi_;
	Float_t deltaGenR_, closestJetToMuonGenPt_,closestJetToElecGenPt_, mt_, mtw_, mtwElec_, genPt_, genPhi_, genEta_, genDeltaR_, genPTJet_, genPTRelJet_;
	// reco iso eff plots

	//Varialbes used for studies
	Float_t RecoMuonDeltaR_, RecoMuonPTJet_, RecoMuonPTRelJet_, IsoMuonDeltaR_, IsoMuonPTJet_, IsoMuonPTRelJet_, RecoGenMuDeltaR_;
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

	// gen values for top b tagging
	int nTop_, nTopB_, nTopW_, nTopMuNu_, nTopMu_, nTopElec_;
	Float_t TopPT_, BTopPT_, WTopPT_, MuNuTopPT_, MuTopPT_, ElecTopPT_;
	Float_t TopEta_, BTopEta_, WTopEta_, MuNuTopEta_, MuTopEta_, ElecTopEta_;
	Float_t TopPhi_, BTopPhi_, WTopPhi_, MuNuTopPhi_, MuTopPhi_, ElecTopPhi_;

	Float_t promtMuMetCombinedPT_, promtMuMetCombinedEta_, promtMuMetCombinedPhi_;
	Float_t wTopMassDifRecoGenPt_, wTopMassDifRecoGenEta_, wTopMassDifRecoGenPhi_;

	Float_t BMuTopDeltaR_, mtt_;
	Float_t recoMtw1_,recoMtw2_,recoMtw3_,recoMtw4_,recoMtw5_;
	Float_t recoMuDeltaPTClosestJet1_, recoMuDeltaPTClosestJet2_, recoMuDeltaPTClosestJet3_, recoMuDeltaPTClosestJet4_, recoMuDeltaPTClosestJet5_;
	Float_t recoMuDeltaRClosestJet1_, recoMuDeltaRClosestJet2_, recoMuDeltaRClosestJet3_, recoMuDeltaRClosestJet4_, recoMuDeltaRClosestJet5_;
	TLorentzVector promtRecoTLVMu_,promtRecoTLVMET_, promtRecoTLVWDecay_, mttRecoMuMet_, mttGen_;

	Float_t nonPromtMuPt_[10],nonPromtMuEta_[10], nonPromtMuPhi_[10], nonPromtMuDeltaR_[10], nonPromtMuDeltaPT_[10];
	int nonPromtMu_[10];
	Float_t MHTJetsPT_[20], MHTJetsEta_[20], MHTJetsPhi_[20];
	int nomMHTJets_, nomNonPromtMu_;


};