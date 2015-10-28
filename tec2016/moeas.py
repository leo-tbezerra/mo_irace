from translator import AutoMOEATranslator
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

    self.cand_params["pop_size"] = args[3].split("=")[1]
    nb_offspring = AutoMOEATranslator._parseRatio(self.cand_params["pop_size"], args[4])
    self.cand_params["nb_offspring"] = "{:.0f}".format(nb_offspring)

    super()._parseEngine(args[5:])
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

    self.cand_params["pop_size"] = args[3].split("=")[1]
    super()._parseEngine(args[5:])
    sigma = self._consumeParam(args, False)
    if self.cand_params["engine"] == "GA":
      self.cand_params["pop_diversity"] = "Sharing({})".format(sigma)
    else:
      self.cand_params["pop_diversity"] = "Dummy"

    super()._cmdLine()
