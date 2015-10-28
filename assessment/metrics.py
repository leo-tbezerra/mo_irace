from abc import ABCMeta, abstractmethod
import subprocess, os

class Metric(metaclass=ABCMeta):
  @abstractmethod
  def _compute(self):
    return

  @abstractmethod
  def _setup(self, _nobj, _bound):
    return

class hvRPD(Metric):
  refpoint = []
  def _setup(self, _nobj, _bound):
    self.refpoint = []
    refpoint = _bound * 1.1
    for i in range(0, _nobj):
      self.refpoint.append(refpoint)
      
  def _compute(self, _front_file, _ref_file, _in_ext="_dat", _out_ext="_rpd"):
    front_file = "{}{}".format(_front_file, _in_ext)
    front_handler = open(front_file, "r")
    hv_file = "{}_hv".format(front_file)
    hv_handler = open(hv_file, "w+")

    subprocess.call(["/home/lbezerra/bin/hv", "-r {}".format(' '.join(str(e) for e in self.refpoint))], stdin=front_handler, stdout=hv_handler, stderr=subprocess.PIPE)
    if os.stat(hv_file).st_size > 0:
      hv_handler.seek(0)
      run_hv = float(hv_handler.read())
      ref_handler = open(_ref_file, "r")
      ref_hv = float(ref_handler.read())
      hv_rpd = (ref_hv - run_hv) / ref_hv
    else:
      hv_rpd = 5
    front_handler.close()
    hv_handler.close()
    os.unlink("{}_hv".format(front_file))
    return hv_rpd

class unEps(Metric):
  def _setup(self, _nobj, _bound):
    return
  def _compute(self, _front_file, _ref_file, _extension="_eps"):
    super()._compute()
    front_handler = open(_front_file, "r")
    eps_file = "{}{}".format(_front_file, _extension)
    eps_handler = open(eps_file, "w+")
    subprocess.call("/home/lbezerra/bin/epsilon -r {} < {} > {}".format(_ref_file, _front_file, eps_file), shell=True)
    if os.stat(eps_file).st_size > 0:
      eps_handler.seek(0)
      un_eps = float(eps_handler.read())
    else:
      un_eps = 25000
    eps_handler.close()
    os.unlink(eps_file)
    return un_eps
