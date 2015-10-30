class Translator:
  params = {}
  extra_params = ""
  def __init__(self, _extra_params):
    self.extra_params = _extra_params
  def _translate(self):
    translated_params = ""
    for key in self.params.keys():
      translated_params += "{}{} ".format(self.params[key][0], self.params[key][1])
    return self.problem_params + translated_params + self.extra_params

class OrderedTranslator(Translator):
  order = ()
  def __init__(self, _problem_params, _cand_params, _fixed_params, _extra_params):
    self.params = _problem_params.copy()
    self.params.update(_cand_params)
    self.params.update(_fixed_params)
    self.params.update(_extra_params)

  def _translate(self):
    cmdline = ""
    for key in self.order:
      if key in self.params:
        cmdline += " {}".format(self.params[key])
    return cmdline
  
class MOEADTranslator(OrderedTranslator):
  order = ("problem", "size", "nobj", "pop_size", "niche_ratio", "delta", "limit", "tsize", "nu", "engine", "de_cr", "de_f", 
            "cross_rate", "eta_cross", "mut_rate", "mut_vrate", "eta_mut","aggregation", "pbi_penalty", "seed", "evals", "weight_set")

class CMASharkTranslator(OrderedTranslator):
  order = ("problem", "nobj", "size", "evals", "time", "seed", "pop_size", "sigma", "notion", "indicator", "steady")

class AutoMOEATranslator(Translator):
  all_params = {"pop_size": ["--popSize=", 0], "nb_offspring": ["--nbOffspring=", "100%"], "pop_select": ["--popSelection=", "Random"],
            "pop_setpart": ["--popSetPart=", "Dummy"], "pop_refinement": ["--popRefinement=", "Dummy"], "pop_diversity": ["--popDiversity=", "Dummy"], 
            "engine": ["--evolutionEngine=", "GA"], "de_cr": ["--CR=", 0.1], "de_f": ["--F=", 1.0],
            "cross_rate": ["--pCross=", "0.1"], "eta_cross": ["--etaCross=", 5], "mut_rate": ["--pMut=", 0.1], "mut_vrate": ["--vMut=", 0.01], "eta_mut": ["--etaVar=", 50],
            "use_archive": ["--useArchive=", 0], "fixed_size": ["--fixedSizeInternalArchive=", 1], 
            "internal_setpart": ["--internalArchiveSetPart=", "Dummy"], 
            "internal_refinement": ["--internalArchiveRefinement=", "Dummy"], 
            "internal_diversity": ["--internalArchiveDiversity=", "Dummy"], 
            "internal_replacement": ["--internalArchiveReplacement=", "Elitist"],
            "evals": ["--maxEval=", 0], "time": ["--maxTime=", 0],
            "gen": ["--maxGen=", 0], "seed": ["--seed=", 0]}

  def __init__(self, _problem_params, _fixed_params, _cand_params, _extra_params):
    super().__init__(_extra_params)
    self.problem_params = "--MOP={} --nVar={} ".format(_problem_params['problem'], _problem_params['size']) 
    for key in _fixed_params.keys():
      self.params[key] = [self.all_params[key][0], _fixed_params[key]]
    for key in _cand_params.keys():
      self.params[key] = [self.all_params[key][0], _cand_params[key]]

  @classmethod
  def _parse_arg(_cls, _args, _params, _triggers):
    cur_arg = _args[0]
    cur_p = _params[0]
    if len(cur_p) == 1:
      key = cur_p[0]
      _triggers.append(_cls.params[key][0])
    if len(_args) > 1:
      _cls._parse_arg(_args[1:], _params[1:], _triggers)

  @classmethod
  def _parse(_cls, _args, _params):
    triggers = []
    _cls._parse_arg(_args, _params, triggers)
    print ("triggers")
    for key in triggers:
      print("{}".format(key))
    return { "pop_size": 10, "nb_offspring": "130%" }

  @classmethod
  def _parseRatio(_cls, _base, _ratio):
    return float(_base) * float(_ratio)
