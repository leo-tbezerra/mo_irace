from abc import ABCMeta, abstractmethod
import subprocess, os, sys

class Metric(metaclass=ABCMeta):
  @abstractmethod
  def _compute(self):
    return

  @abstractmethod
  def _setup(self, _nobj, _bound):
    return

class hvRPD(Metric):
  def _setup(self, _nobj, _bound):
    refpoint = _bound * 1.1
    self.hv = PaGMO()
    self.hv._setup(_nobj, refpoint)
      
  def _compute(self, _front_file, _ref_file, _out_ext="_rpd"):
    run_hv = self.hv._compute(_front_file, _ref_file)
    if run_hv == -12.3:
      hv_rpd = 5
    else:
      ref_handler = open(_ref_file, "r")
      ref_hv = float(ref_handler.read())
      hv_rpd = (ref_hv - run_hv) / ref_hv
    return hv_rpd

# Hypervolume implementation by Fonseca, Paquete and Lopez-Ibanez
class FPL(Metric):
  refpoint = []
  def _setup(self, _nobj, _refpoint):
    self.refpoint = []
    for i in range(0, _nobj):
      self.refpoint.append(_refpoint)
      
  def _compute(self, _front_file, _ref_file, _out_ext="_hv"):
    front_handler = open(_front_file, "r")
    hv_file = "{}_hv".format(_front_file)
    hv_handler = open(hv_file, "w+")

    subprocess.call(["/home/lbezerra/bin/hv", "-r {}".format(' '.join(str(e) for e in self.refpoint))], stdin=front_handler, stdout=hv_handler, stderr=subprocess.PIPE)
    
    if os.stat(hv_file).st_size > 0:
      hv_handler.seek(0)
      run_hv = float(hv_handler.read())
    else:
      front_handler.close()
      hv_handler.close()
      os.unlink(hv_file)
      sys.exit(-1)

    front_handler.close()
    hv_handler.close()
    os.unlink(hv_file)
    return run_hv

# Hypervolume implementation by Walking-Fish Group provided by PaGMO
class PaGMO(Metric):
  nobj = 0
  refpoint = 0.0
  def _setup(self, _nobj, _refpoint):
    self.nobj = _nobj
    self.refpoint = _refpoint

  def _compute(self, _front_file, _ref_file, _out_ext="_hv"):
    hv_file = "{}_hv".format(_front_file)
    hv_handler = open(hv_file, "w+")

    subprocess.call(["/home/lbezerra/bin/HV", "--frontFile={}".format(_front_file), "--nObj={}".format(self.nobj), "--refPoint={}".format(self.refpoint)], stdout=hv_handler, stderr=subprocess.PIPE)
    if os.stat(hv_file).st_size > 0:
      hv_handler.seek(0)
      run_hv = float(hv_handler.read())
    else:
      hv_handler.close()
      os.unlink(hv_file)
      sys.exit(-1)

    hv_handler.close()
    os.unlink(hv_file)
    return run_hv

class unEps(Metric):
  def _setup(self, _nobj, _bound):
    return
  def _compute(self, _front_file, _ref_file, _extension="_eps"):
    front_handler = open(_front_file, "r")
    eps_file = "{}{}".format(_front_file, _extension)
    eps_handler = open(eps_file, "w+")
    subprocess.call("/home/lbezerra/bin/epsilon -r {} < {} > {}".format(_ref_file, _front_file, eps_file), shell=True)
    if os.stat(eps_file).st_size > 0:
      eps_handler.seek(0)
      un_eps = float(eps_handler.read())
    else:
      eps_handler.close()
      os.unlink(eps_file)
      sys.exit(-1)
    eps_handler.close()
    os.unlink(eps_file)
    return un_eps

class IGD(Metric):
  def _setup(self, _nobj):
    self.nobj = _nobj
  def _compute(self, _front_file, _ref_file, _extension="_igd"):
    igd_file = "{}{}".format(_front_file, _extension)
    igd_handler = open(igd_file, "w+")
   
    subprocess.call(["/home/lbezerra/bin/IGD", "--frontFile={}".format(_front_file), "--nObj={}".format(self.nobj), "--refFile={}".format(_ref_file)], stdout=igd_handler, stderr=subprocess.PIPE)
    if os.stat(igd_file).st_size > 0:
      igd_handler.seek(0)
      igd = float(igd_handler.read())
    else:
      igd_handler.close()
      os.unlink(igd_file)
      sys.exit(-1)

    igd_handler.close()
    os.unlink(igd_file)
    return igd

