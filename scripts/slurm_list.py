#!/usr/bin/python3
 
import sys
import os
from slurm import send_sbatch 

jtime = '3:0:0'
cpus = 4

ifile = str(sys.argv[1])
wdir = 'slurm'
if not os.path.isdir(wdir): os.mkdir(wdir)
count = 0
ljob = {'job_name':ifile, 'cpus':cpus, 'mem_per_cpu':'4G', 'time':jtime, 'output':wdir+'/'+ifile+'order-%j', 'mailtype':'FAIL,TIME_LIMIT,STAGE_OUT'}
with open(ifile, 'r') as orf:
  for line in orf:
    count+=1
    ljob['filename'] = wdir+'/sorder_{:04d}'.format(count)+'.sh'
    ljob['command'] = line
    send_sbatch(ljob)
ejob = {'job_name':ifile, 'output':wdir+'/'+ifile+'end-%j', 'filename':wdir+'/sorder_end.sh', 'dependency':'singleton'}
send_sbatch(ejob)
