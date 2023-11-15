#!/usr/bin/env python

"""
Copyright 2020 O. Sotolongo <asqwerty@gmail.com>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""
import os
import subprocess
import random

def default_job():
  task = {'mem_per_cpu':'4G', 'cpus':1, 'time':'2:0:0', 'job_name':'myjob', 'mailtype':'FAIL,TIME_LIMIT,STAGE_OUT'}
  task['filename'] = 'slurm_{:03d}.sh'.format(random.randint(0,1000))
  task['output'] = 'slurm_{:03d}.out'.format(random.randint(0,1000))
  task['order'] = 'sbatch --parsable '+task['filename']
  return task

def send_sbatch(env_data):
  """
  This function creates and executes an sbatch script into SLURM
 
  It takes a dict with the required environment data and returns
  the jobid of the task
  """
  content = '#!/bin/bash\n'
  def_data = default_job()
  if 'job_name' in env_data:
    content += '#SBATCH -J '+env_data['job_name']+'\n'
  else:
    content += '#SBATCH -J '+def_data['job_name']+'\n'
  if 'cpus' in env_data:
    content += '#SBATCH -c '+str(env_data['cpus'])+'\n'
    if 'mem-per-cpu' in env_data:
        env_data['mem_cpu'] = env_data['mem-per-cpu']
    if 'mem_cpu' in env_data:
      content += '#SBATCH --mem-per-cpu='+env_data['mem_cpu']+'\n'
    else:
      content += '#SBATCH --mem-per-cpu='+def_data['mem_cpu']+'\n'
  if 'ntask_node' in env_data: content += '#SBATCH --ntaks-per-node='+env_data['ntask_node']+'\n'
  if 'time' in env_data: 
    content += '#SBATCH --time='+env_data['time']+'\n'
  else:
    content += '#SBATCH --time='+def_data['time']+'\n'
  content += '#SBATCH --mail-user='+os.environ.get('USER')+'\n'
  if 'output' in env_data: 
    content += '#SBATCH -o '+env_data['output']+'-%j\n'
  else:
    content += '#SBATCH -o '+def_data['output']+'-%j\n'
  if 'partition' in env_data: content += '#SBATCH -p '+env_data['partition']+'\n'
  if 'gres' in env_data: content += '#SBATCH --gres='+env_data['gres']+'\n'
  if 'command' in env_data:
    if 'mailtype' in env_data:
      content += '#SBATCH --mail-type='+env_data['mailtype']+'\n'
    else:
      content += '#SBATCH --mail-type='+def_data['mailtype']+'\n'
    content += env_data['command']+'\n'
  else:
    content += '#SBATCH --mail-type=END\n'
    content += ':\n'
  if 'filename' in env_data:
    filename = env_data['filename']
  else:
    filename = def_data['filename']
  f = open(filename, 'w')
  f.write(content)
  f.close()
  if 'dependency' in env_data:
    order = ['sbatch --parsable --dependency='+env_data['dependency']+' '+filename]
  else:
    if 'filename' in env_data:
      order = 'sbatch --parsable '+filename
    else:
      order = def_data['order']
  if 'test' in env_data and env_data['test']:
    return 0
  else:
    return int(subprocess.check_output(order, shell=True))

