from abc import ABCMeta, abstractmethod
from translator import *

import subprocess, os, sys

class HookRun(metaclass=ABCMeta):
  cand_params = {}
  problem_params = {"problem": "", "size": 0, "nobj": 0, "seed": 0}
  fixed_params = {"evals": 0, "time": 0, "gen": 0}
  extra_params = ""
  command_line = ""
  stdout, stderr, stdlog = "", "", ""
  problem_name = ""

  def __init__(self, _algo, _nobj, _exe, _evals, _time, _gen, _translator, _assesser, _irace):
    self.algo = _algo
    self.nobj = _nobj
    self.exe = _exe
    self.fixed_params["evals"]  = _evals
    self.fixed_params["time"] = _time
    self.fixed_params["gen"] = _gen
    self.translator = _translator
    self.assesser = _assesser
    self.irace = _irace["flag"]
    self.irace_metric = _irace["metric"]

  def _print(self):
    print(self.command_line)

  def _run(self):
    outfile = open(self.stdout, "w") 
    errfile = open(self.stderr, "w")
    logfile = open(self.stdlog, "w")
    logfile.write("{} {}".format(self.exe, self.command_line))
    subprocess.call("{} {}".format(self.exe, self.command_line), stdout=outfile, stderr=errfile, shell=True)

    results = self.assesser._compute(self.stdout, "{}.hv".format(self.problem_name), "{}.front".format(self.problem_name))

    if self.irace:
      print(results[self.irace_metric])
      return
      os.unlink(self.stdout)
      os.unlink(self.stderr)
      os.unlink(self.stdlog)
    else:
      for key, value in results.items():
        out_file = "{}_{}".format(self.stdout, key)
        out_handler = open(out_file, "w")
        out_handler.write("{}\n".format(value))
        out_handler.close()

  def _cmdLine(self):
    _translator = self.translator(self.problem_params, self.fixed_params, self.cand_params, self.extra_params)
    self.command_line = _translator._translate()

  def _consumeParam(self, _args):
    value = None
    if '=' in _args[0]:
      value = _args[0].split("=")[1]
    else:
      value = _args[0]
    _args.pop(0)
    return value
        
  @abstractmethod
  def _parse(self, args):
    split1 = args[0].split("@")
    split2 = split1[0].split("_")

    problem = split2[0]
    size = int(split2[1])
    nobj = int(split1[1])
    cand_id = args[1]
    seed = args[2]

    if (self.nobj != nobj):
      print("Error! Problem's #objectives (%d) different from class's (%d)!" % (nobj, self.nobj))
      sys.exit(-1)

    basename = "c{}-{}-{}-{}-{}".format(cand_id, seed, problem, nobj, size)
    self.problem_name = "{}.{}.{}".format(problem, nobj, size)
    if self.irace:
      if not os.path.exists("arena"):
        os.mkdir("arena")
      self.stdout = "arena/{}.stdout".format(basename)
      self.stderr = "arena/{}.stderr".format(basename)
      self.stdlog = "arena/{}.stdlog".format(basename)
    else:
      self.stdout = "{}.stdout".format(basename)
      self.stderr = "{}.stderr".format(basename)
      self.stdlog = "{}.stdlog".format(basename)

    self.problem_params["problem"] = problem
    self.problem_params["size"] = size
    self.problem_params["nobj"] = nobj
    self.cand_params["seed"] = seed

