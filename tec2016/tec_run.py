from hook_run import HookRun
from tec2016.assesser import TECAssesser

class TECHookRun(HookRun):
  def __init__ (self, _algo, _nobj, _exe, _evals, _time, _irace, _gen):
    assesser = TECAssesser(_nobj, _irace = _irace)
    super().__init__(_algo, _nobj, _exe, _evals, _time, _gen, "Paradiseo", assesser, _irace)

  def _consumeParam(self, _args, _preffix = True):
    value = None
    if _preffix:
      value = _args[0].split("=")[1]
    else:
      value = _args[0]
    _args.pop(0)
    return value

  def _parseEngine(self, args, _tsize = True):
    engine = self._consumeParam(args)
    if engine == "GA":
      if _tsize: 
        tsize = self._consumeParam(args, False)
        self.cand_params["pop_select"] = "DetTour({})".format(tsize)
      else:
        self.cand_params["pop_select"] = "Random"

      self.cand_params["cross_rate"] = self._consumeParam(args)
      self.cand_params["eta_cross"] = self._consumeParam(args)
      self.cand_params["mut_rate"] = self._consumeParam(args)

      single_bit = self._consumeParam(args, False)
      if single_bit == "1":
        self.cand_params["mut_vrate"] = "{:.4f}".format(1.0 / self.problem_params["size"])
      else:
        self.cand_params["mut_vrate"] = self._consumeParam(args, False)
      self.cand_params["eta_mut"] = self._consumeParam(args)

    else:
      self.cand_params["pop_select"] = "Random"
      self.cand_params["de_cr"] = self._consumeParam(args)
      self.cand_params["de_f"] = self._consumeParam(args)
    self.cand_params["engine"] = engine
