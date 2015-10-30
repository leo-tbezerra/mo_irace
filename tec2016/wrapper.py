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

handler = None
handlers = { "ibea": IBEAHookRun, "moga": MOGAHookRun, "hype" : HypeHookRun, "nsga": NSGA2HookRun, "spea": SPEA2HookRun, "sms": SMSHookRun }
handler = handlers[algo](nobj, "/home/lbezerra/bin/AutoMOEA-continuous-{}D".format(nobj), evals, time, _irace = irace)
#if algo = "ibea":
#  handler = IBEAHookRun(nobj, "/home/lbezerra/bin/AutoMOEA-continuous-3D", evals, time, _irace = irace)
#elif algo = "moga":
#  handler = MOGAHookRun(nobj, "/home/lbezerra/bin/AutoMOEA-continuous-3D", evals, time, _irace = irace)

handler._parse(sys.argv[offset:])
handler._run()
