from translator import AutoMOEATranslator, MOEADTranslator, CMASharkTranslator
from tec2016.tec_run import TECHookRun
class IBEAHookRun(TECHookRun):
  def __init__(self, _nobj, _exe, _evals, _time, _irace, _gen=0):
    super().__init__("IBEA", _nobj, _exe, _evals, _time, _irace, _gen)
    self.fixed_params["use_archive"] = 0
    self.fixed_params["fixed_size"] = 1
    self.fixed_params["internal_setpart"] = "Dummy"
    self.fixed_params["internal_refinement"] = "IndicatorBased(Epsilon)"
    self.fixed_params["internal_diversity"] = "Dummy"
    self.fixed_params["internal_replacement"] = "Environmental"
    self.fixed_params["pop_setpart"] = "Dummy"
    self.fixed_params["pop_diversity"] = "Dummy"

  def _parse(self, args):
    super()._parse(args[0:3])
    args = args[3:]    
    self.cand_params["pop_size"] = self._consumeParam(args)
    nb_offspring_ratio = self._consumeParam(args)
    nb_offspring = AutoMOEATranslator._parseRatio(self.cand_params["pop_size"], nb_offspring_ratio)
    self.cand_params["nb_offspring"] = "{:.0f}".format(nb_offspring)
    super()._parseEngine(args)
    if self.cand_params["engine"] == "GA":
      self.cand_params["pop_refinement"] = "IndicatorBased(Epsilon)"
    else:
      self.cand_params["pop_refinement"] = "Dummy"
    super()._cmdLine()

class MOGAHookRun(TECHookRun):
  def __init__(self, _nobj, _exe, _evals, _time, _irace, _gen=0):
    super().__init__("MOGA", _nobj, _exe, _evals, _time, _irace, _gen)
    self.fixed_params["use_archive"] = 0
    self.fixed_params["fixed_size"] = 1
    self.fixed_params["internal_setpart"] = "Dummy"
    self.fixed_params["internal_refinement"] = "Dummy"
    self.fixed_params["internal_diversity"] = "Dummy"
    self.fixed_params["internal_replacement"] = "Generational"
    self.fixed_params["pop_setpart"] = "DomRank"
    self.fixed_params["pop_refinement"] = "Dummy"
    self.fixed_params["nb_offspring"] = "100%"

  def _parse(self, args):
    super()._parse(args[0:3])
    args = args[3:]    
    self.cand_params["pop_size"] = self._consumeParam(args)
    super()._parseEngine(args)
    if self.cand_params["engine"] == "GA":
      sigma = self._consumeParam(args)
      self.cand_params["pop_diversity"] = "Sharing({})".format(sigma)
    else:
      self.cand_params["pop_diversity"] = "Dummy"
    super()._cmdLine()

class HypeHookRun(TECHookRun):
  def __init__(self, _nobj, _exe, _evals, _time, _irace, _gen=0):
    super().__init__("HypE", _nobj, _exe, _evals, _time, _irace, _gen)
    self.fixed_params["use_archive"] = 0
    self.fixed_params["fixed_size"] = 1
    self.fixed_params["internal_setpart"] = "DomDepth"
    self.fixed_params["internal_refinement"] = "PropHypervolumeContribution"
    self.fixed_params["internal_diversity"] = "Dummy"
    self.fixed_params["internal_replacement"] = "Environmental"
    self.fixed_params["pop_setpart"] = "Dummy"
    self.fixed_params["pop_diversity"] = "Dummy"

  def _parse(self, args):
    super()._parse(args[0:3])
    args = args[3:]
    self.cand_params["pop_size"] = self._consumeParam(args)
    nb_offspring_ratio = self._consumeParam(args)
    nb_offspring = AutoMOEATranslator._parseRatio(self.cand_params["pop_size"], nb_offspring_ratio)
    self.cand_params["nb_offspring"] = "{:.0f}".format(nb_offspring)
    super()._parseEngine(args)
    if self.cand_params["engine"] == "GA":
      self.cand_params["pop_refinement"] = "PropHypervolumeContribution"
    else:
      self.cand_params["pop_refinement"] = "Dummy"
    super()._cmdLine()

class NSGA2HookRun(TECHookRun):
  def __init__(self, _nobj, _exe, _evals, _time, _irace, _gen=0):
    super().__init__("NSGA-II", _nobj, _exe, _evals, _time, _irace, _gen)
    self.fixed_params["use_archive"] = 0
    self.fixed_params["fixed_size"] = 1
    self.fixed_params["internal_setpart"] = "DomDepth"
    self.fixed_params["internal_refinement"] = "Dummy"
    self.fixed_params["internal_diversity"] = "Crowding"
    self.fixed_params["internal_replacement"] = "Elitist"
    self.fixed_params["pop_refinement"] = "Dummy"

  def _parse(self, args):
    super()._parse(args[0:3])
    args = args[3:]
    self.cand_params["pop_size"] = self._consumeParam(args)
    nb_offspring_ratio = self._consumeParam(args)
    nb_offspring = AutoMOEATranslator._parseRatio(self.cand_params["pop_size"], nb_offspring_ratio)
    self.cand_params["nb_offspring"] = "{:.0f}".format(nb_offspring)
    super()._parseEngine(args)
    if self.cand_params["engine"] == "GA":
      self.cand_params["pop_setpart"] = "DomDepth"
      self.cand_params["pop_diversity"] = "Crowding"
    else:
      self.cand_params["pop_setpart"] = "Dummy"
      self.cand_params["pop_diversity"] = "Dummy"
    super()._cmdLine()

class SPEA2HookRun(TECHookRun):
  def __init__(self, _nobj, _exe, _evals, _time, _irace, _gen=0):
    super().__init__("SPEA2", _nobj, _exe, _evals, _time, _irace, _gen)
    self.fixed_params["use_archive"] = 0
    self.fixed_params["fixed_size"] = 1
    self.fixed_params["internal_setpart"] = "DomCountRank"
    self.fixed_params["internal_refinement"] = "Dummy"
    self.fixed_params["internal_diversity"] = "kNN"
    self.fixed_params["internal_replacement"] = "Environmental"
    self.fixed_params["pop_setpart"] = "DomCountRank"
    self.fixed_params["pop_refinement"] = "Dummy"
    self.fixed_params["nb_offspring"] = "100%"

  def _parse(self, args):
    super()._parse(args[0:3])
    args = args[3:]
    self.cand_params["pop_size"] = self._consumeParam(args)
    nb_offspring_ratio = self._consumeParam(args)
    nb_offspring = AutoMOEATranslator._parseRatio(self.cand_params["pop_size"], nb_offspring_ratio)
    self.cand_params["nb_offspring"] = "{:.0f}".format(nb_offspring)
    super()._parseEngine(args)
    if self.cand_params["engine"] == "GA":
      auto_k = self._consumeParam(args)
      if auto_k == "0":
        k = self._consumeParam(args)
        self.cand_params["pop_diversity"] = "kNN({})".format(k)
      else:
        self.cand_params["pop_diversity"] = "kNN"
    else:
      self.cand_params["pop_diversity"] = "Dummy"
    super()._cmdLine()

class SMSHookRun(TECHookRun):
  def __init__(self, _nobj, _exe, _evals, _time, _irace, _gen=0):
    super().__init__("SMS-EMOA", _nobj, _exe, _evals, _time, _irace, _gen)
    self.fixed_params["use_archive"] = 0
    self.fixed_params["fixed_size"] = 1
    self.fixed_params["internal_setpart"] = "DomDepth"
    self.fixed_params["internal_refinement"] = "HypervolumeContribution"
    self.fixed_params["internal_diversity"] = "Dummy"
    self.fixed_params["internal_replacement"] = "Environmental"
    self.fixed_params["pop_setpart"] = "Dummy"
    self.fixed_params["pop_refinement"] = "Dummy"
    self.fixed_params["pop_diversity"] = "Dummy"
    self.fixed_params["nb_offspring"] = "100%"

  def _parse(self, args):
    super()._parse(args[0:3])
    args = args[3:]
    self.cand_params["pop_size"] = self._consumeParam(args)
    super()._parseEngine(args, False)
    super()._cmdLine()

class MOEADHookRun(TECHookRun):
  def __init__(self, _nobj, _exe, _evals, _time, _irace, _gen=0):
    super().__init__("MOEA/D", _nobj, _exe, _evals, _time, _irace, _gen, _translator = MOEADTranslator)
    self.fixed_params["weight_set"] = "/home/lbezerra/bin/moead_weights/W{}D.dat".format(_nobj)

  def _parse(self, args):
    super()._parse(args[0:3])
    args = args[3:]
    self.cand_params["pop_size"] = self._consumeParam(args)
    self.cand_params["niche_ratio"] = self._consumeParam(args)
    self.cand_params["delta"] = self._consumeParam(args)
    self.cand_params["limit"] = self._consumeParam(args)
    self.cand_params["tsize"] = self._consumeParam(args)
    self.cand_params["nu"] = self._consumeParam(args)
    super()._parseEngine(args, False)
    del(self.cand_params["pop_select"])
    self.cand_params["aggregation"] = self._consumeParam(args)
    if self.cand_params["aggregation"] == "PBI":
      self.cand_params["pbi_penalty"] = self._consumeParam(args)
    super()._cmdLine()

class CMAHookRun(TECHookRun):
  def __init__(self, _nobj, _exe, _evals, _time, _irace, _gen=0):
    super().__init__("MO-CMA-ES", _nobj, _exe, _evals, _time, _irace, _gen, _translator = CMASharkTranslator)

  def _parse(self, args):
    super()._parse(args[0:3])
    args = args[3:]
    self.cand_params["pop_size"] = self._consumeParam(args)
    self.cand_params["sigma"] = self._consumeParam(args)
    self.cand_params["notion"] = self._consumeParam(args)
    self.cand_params["indicator"] = self._consumeParam(args)
    self.cand_params["steady"] = self._consumeParam(args)
    super()._cmdLine()
