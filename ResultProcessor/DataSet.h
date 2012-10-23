#ifndef DATA_SET_H
#define DATA_SET_H

#include <map>
#include <set>
#include <vector>

#include "TString.h"

#include "Config.h"
#include "Event.h"



class DataSet {
public:
  enum Type { Data, MC, Bkg, Signal };

  static std::vector<DataSet*> createDataSets(const Config &cfg, const TString key);
  static bool exists(const TString &label);
  static Type type(const TString &label);
  static Type toType(const TString &type);

  virtual ~DataSet();

  Type type() const { return type_; }
  TString label() const { return label_; }
  TString selection() const { return selectionLabel_; }
  double weightScale() const { return weightScale_; }

  unsigned int size() const { return evts_.size(); }
  EventIt begin() const { return evts_.begin(); }
  EventIt end() const { return evts_.end(); }

  void selection(const TString &selection) {
    selectionLabel_ = selection;
  }


protected:
  DataSet(Type type, const TString &label, const TString &selection, const Events &evts, double weightScale);	// This constructor is meant for use in SelectedDataSet


private:
  static std::set<TString> labels_;
  static std::map<TString,DataSet::Type> types_;

  const Type type_;
  const TString label_;
  const double weightScale_;	// Each event has a weight from the tree times weightScale_
  const bool hasMother_;

  TString selectionLabel_;
  Events evts_;

  DataSet(Type type, const TString &label, const TString &selection, const TString &fileName, const TString &treeName, const TString &weightVarName, double weightScale);
};


class SelectedDataSet : public DataSet {
public:
  SelectedDataSet(Type type, const TString &label, const TString &selection, const Events &evts, double weightScale)
    : DataSet(type,label,selection,evts,weightScale) {};
  ~SelectedDataSet() {};
};
#endif
