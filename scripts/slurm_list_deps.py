#!/usr/bin/env python
import sys
import os 
import re

from slurm import send_sbatch

jtime = '3:0:0'
cpus = 4
mem_per_cpu = '4G'

ifile = str(sys.argv[1])
wdir = 'slurm'
if not os.path.isdir(wdir): os.mkdir(wdir)
count = 0
precedence = 1
ljob = {'job_name':ifile, 'cpus':cpus, 'mem_per_cpu':mem_per_cpu, 'time':jtime, 'output':wdir+'/'+ifile+'order-%j', 'mailtype':'FAIL,TIME_LIMIT,STAGE_OUT'}

with open(ifile, 'r') as orf:
  for line in orf:
    count+=1
    order = re.search(r"(\d+):(.*)", line)
    norder = int(order.group(1))
    ljob['filename'] = wdir+'/sorder_{:04d}'.format(count)+'.sh'
    ljob['command'] = order.group(2)
    if norder > precedence:
      ljob['dependency'] = 'afterok:'+str(jobid)
    else:
      ljob.pop('dependency', None)
    jobid = send_sbatch(ljob)
    precedence = norder
ejob = {'job_name':ifile, 'output':wdir+'/'+ifile+'end-%j', 'filename':wdir+'/sorder_end.sh', 'dependency':'singleton'}
send_sbatch(ejob)


