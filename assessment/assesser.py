import os, subprocess
class Assesser():
  persist = True
  bounds = {}
  def __init__(self, _nobj, _filter = None, _hv = None, _eps = None, _igd = None, _persist = True):
    self.nobj = _nobj
    self.filter = _filter
    self.metrics = { "rpd": _hv, "eps": _eps, "igd": _igd }
    self.defaults = { "rpd": 5, "eps": 25000, "igd": 25000 }
    self.persist = _persist

  def _compute(self, _front_file, _ref_file_hv = "", _ref_file_eps = "", _ref_file_igd = ""):
    front_file = _front_file
    ref_file = {}
    ref_file["rpd"] = self.ref_folder + _ref_file_hv
    ref_file["eps"] = self.ref_folder + _ref_file_eps
    if _ref_file_igd == "": 
      ref_file["igd"] = ref_file["eps"]
    else:
      ref_file["igd"] = self.ref_folder + _ref_file_igd
     
    results = {}
    for key, value in self.metrics.items():
      if not value == None: 
        results[key] = self.defaults[key]

    if not self.filter == None:
      self.filter._filter(_front_file)
      front_file += "_dat"
      output = subprocess.check_output('cat {} | grep "^[0-9]" | wc -l'.format(front_file), shell=True, universal_newlines=True).split('\n')
      empty = output[0] == "0"
      if empty:
        return results

    for key, value in self.metrics.items():
      if not value == None: 
        results[key] = self.metrics[key]._compute(front_file, ref_file[key])

    if not self.persist:
      os.unlink(front_file)
    return results

