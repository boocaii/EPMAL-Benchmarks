# Run applications and record its execution time

import os, sys, datetime, time
from os import path

from collections import namedtuple
import logging, subprocess

PWD = path.dirname(path.realpath(__file__))
kripke_EXE = path.join(PWD, "Kripke", "build", "bin", "kripke.exe")
other_param = kripke_EXE + "--groups 128"
data_FILENAME = "kripke.csv"
# print(Kripke_EXE)


#####################################
# Performance parameters of Kripke
#####################################
# --layout <DGZ, DZG, GDZ, GZD, ZDG, ZGD>
# --gset <1,2,4,8,16,32,64>
# --dset <8,16,32>
# --pmethod <sweep, bj>
# mpirun -n <1,2,4,8,16,32,64,128,256,512>

ParamsName =  ["layout", "gset", "dset", "pmethod", "n_process"]
ParamsRange = namedtuple("ParamsRange", ParamsName)
params_range = ParamsRange(
  layout = ["DGZ", "DZG", "GDZ", "GZD", "ZDG", "ZGD"],
  gset = [1,2,4,8,16,32,64,128],
  dset = [8,16,32],
  pmethod = ["sweep","bj"],
  n_process = [1,2,4,8,16,32,64,128]#,256,512]
)
Param = namedtuple("Param", ParamsName)
#print(params_range)

def gen_params():
  params = []
  values = []

  def _gen_params(param=[], value=[], level=0):
    if level >= len(params_range):
      params.append(Param(*param))
      values.append(value)
      return
    for i in range(len(params_range[level])):
      _gen_params(
        param + [params_range[level][i]], 
        value + [i], 
        level+1
      )
  
  _gen_params()
  #print(len(params), len(values))
  #print(params)
  #print(values)
  return params, values

# gen_params()

def construct_command(param):
  cmd_str = "mpiexec -np %d %s" % (param.n_process, kripke_EXE)
  for i in range(len(ParamsName)-1):
    cmd_str += " --%s %s" % (ParamsName[i], str(param[i]))
  cmd_str += " --procs %d,1,1" % param.n_process
  cmd_str += " --groups 128"
  cmd_str += " --zones 128,16,16"
  cmd_str += " --niter 2"
  return cmd_str

def run_and_record(cmd):
  try:
    logging.info("COMMAND: %s" % cmd)
    before = time.time()
    cp = subprocess.run(cmd, shell=True, encoding="utf-8", \
      stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    after = time.time()
  except subprocess.SubprocessError:
    # Run fails
    logging.error("EXCEPTION OCCURRED! RETURNCODE: %d, STDOUT: %s, STDERR: %s" \
      % (cp.returncode, cp.stdout, cp.stderr))
    sys.exit(1)
  # Run success
  logging.info("COMPLETED! ELAPSED TIME: %f, RETURNCODE: %d, STDOUT: %s, STDERR: %s" \
    % (after-before, cp.returncode, cp.stdout, cp.stderr))
  exe_time = -1 if cp.returncode != 0 else (after - before)
  return exe_time
  
def write2file(text, first=False):
  mode = "w" if first else "a"
  with open(data_FILENAME, mode) as f:
    f.write(text + "\n")

def main():
  # logging configurations
  log_file = ".kripke-run-%s.log" % datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
  logging.basicConfig( 
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s]\t%(message)s",
    handlers=[
      logging.FileHandler(log_file),
      logging.StreamHandler()
    ]
  )
  logging.info("START RUNNING")
  
  # Generte parameters
  params, _ = gen_params()
  logging.info("Number of params: %d, like this: %s" % (len(params), params[:5]))
  
  # Run Kripke program with all these params one by one
  #if not os.path.exists(data_FILENAME):
  write2file(",".join(ParamsName + ["time"]), True)
  for param in params:
    cmd = construct_command(param)
    exe_time = run_and_record(cmd)
    row_str = ",".join(map(str, param)) + (",%.2f" % exe_time)
    write2file(row_str)
  
  #print(construct_command(params[0]))

  #print(run_and_record("sleep 3"))
  



if __name__ == "__main__":
  main()
