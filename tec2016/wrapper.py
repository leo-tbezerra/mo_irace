import sys
from tec2016.moeas import *

algo = sys.argv[1]
nobj = int(sys.argv[2])
evals = int(sys.argv[3])
time = int(sys.argv[4])

irace = {"flag": True, "metric": "rpd" }
irace["flag"] = sys.argv[5] == "true"
offset = 6

if irace["flag"]:
  irace["metric"] = sys.argv[6]
  offset=7

if algo == "moead":
  bin = "/home/lbezerra/bin/moead_cec"
elif algo == "cma":
  bin = "/home/lbezerra/bin/mo-cma-es"
elif algo == "nsga3":
  bin = "/home/lbezerra/bin/nsga3"
else:
  bin = "/home/lbezerra/bin/AutoMOEA-continuous-{}D".format(nobj)

handler = None
handlers = { "ibea": IBEAHookRun, "moga": MOGAHookRun, "hype" : HypeHookRun, "nsga": NSGA2HookRun, "spea": SPEA2HookRun, "sms": SMSHookRun, 
             "moead": MOEADHookRun, "cma": CMAHookRun, "nsga3": NSGA3HookRun }
handler = handlers[algo](nobj, bin, evals, time, _irace = irace)

handler._parse(sys.argv[offset:])
handler._run()
