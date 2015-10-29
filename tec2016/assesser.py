from assessment.assesser import Assesser
from assessment.filter import MOToolsFilter
from assessment.metrics import hvRPD, unEps, IGD

class TECAssesser(Assesser):
  bounds = { 2: 10, 3: 10, 5: 15, 10: 25 }
  def __init__(self, _nobj, _irace):
    self.bound = self.bounds[_nobj]
    self.ref_folder = "/home/lbezerra/experiments/continuous/cor/fronts/"

    filter = MOToolsFilter()
    filter._setup(_nobj, self.bound)

    irace = _irace["flag"]
    irace_metric = _irace["metric"]
    
    hv, eps, igd = None, None, None
    if not irace:
      hv = hvRPD()
      hv._setup(_nobj, self.bound)
      eps = unEps()
      igd = IGD()
      igd._setup(_nobj)
    if irace:
      if irace_metric == "rpd":
        hv = hvRPD()
        hv._setup(_nobj, self.bound)
      elif irace_metric == "eps":
        eps = unEps()
      elif irace_metric == "igd":
        igd = IGD()
        igd._setup(_nobj)
    
    super().__init__(_nobj, filter, _hv = hv, _eps = eps, _igd = igd, _persist = not irace)

