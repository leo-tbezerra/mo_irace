from abc import ABCMeta, abstractmethod
import subprocess

class Filter(metaclass=ABCMeta):
  args = []
  bound = []
  def _filter(self, _front_file, _extension = "_dat"):
    filtered_file = "{}{}".format(_front_file, _extension)
    filtered_handler = open(filtered_file, "w")
    front_handler = open(_front_file, "r")

    run_filter = subprocess.call(self.args, stdin=front_handler, stdout=filtered_handler)
    return

class MOToolsFilter(Filter):
  def _setup(self, _nobj, _bound):
    self.bound = []
    for i in range(0, _nobj):
      self.bound.append(_bound)
    self.args = ["/home/lbezerra/bin/nondominated", "--filter", "--force-bound",
                                  "--upper-bound={}".format(' '.join(str(e) for e in self.bound))]
