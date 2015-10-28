class Assesser():
  persist = True
  bounds = {}
  def __init__(self, _nobj, _filter = None, _hv = None, _eps = None, _igd = None, _persist = True):
    self.nobj = _nobj
    self.filter = _filter
    self.hv = _hv
    self.eps = _eps
    self.igd = _igd
    self.persist = _persist

  def _compute(self, _front_file, _ref_file_hv = "", _ref_file_eps = ""):
    front_file = _front_file
    ref_file_hv = self.ref_folder + _ref_file_hv
    ref_file_eps = self.ref_folder + _ref_file_eps
    results = {}

    if not self.filter == None:
      self.filter._filter(_front_file)
      front_file += "_dat"

    if not self.hv == None:
      hv_rpd = self.hv._compute(_front_file, ref_file_hv, _in_ext = "_dat", _out_ext = "_rpd")
      results["rpd"] = hv_rpd

    if not self.eps == None:
      un_eps = self.eps._compute(front_file, ref_file_eps)
      results["eps"] = un_eps

    if not self.persist:
      os.unlink(front_file)
    return results

