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

def send_sbatch(env_data):
  """
  This function creates and executes an sbatch script into SLURM
 
  It takes a dict with the required environment data and returns
  the jobid of the task
  """
  content = '#!/bin/bash\n'
  if 'job_name' in env_data:
    content += '#SBATCH -J '+env_data['job_name']+'\n'
  else:
    content += '#SBATCH -J myjob\n'
  if 'cpus' in env_data:
    content += '#SBATCH -c '+str(env_data['cpus'])+'\n'
    if 'mem_cpu' in env_data:
      content += '#SBATCH --mem-per-cpu='+env_data['mem_cpu']+'\n'
    else:
      content += '#SBATCH --mem-per-cpu=4G\n'
  if 'time' in env_data: content += '#SBATCH --time='+env_data['time']+'\n'
  content += '#SBATCH --mail-user='+os.environ.get('USER')+'\n'
  if 'output' in env_data: content += '#SBATCH -o '+env_data['output']+'-%j\n'
  if 'partition' in env_data: content += '#SBATCH -p '+partition+'\n'
  if 'command' in env_data:
    content += '#SBATCH --mail-type=FAIL,TIME_LIMIT,STAGE_OUT\n'
    content += env_data['command']+'\n'
  else:
    content += '#SBATCH --mail-type=END\n'
    content += ':\n'
  if 'filename' in env_data:
    filename = env_data['filename']
  else:
    filename = 'slurm{:03d}.sh'.format(random.randint(0,1000))
  f = open(filename, 'w')
  f.write(content)
  f.close()
  if 'dependency' in env_data:
    order = ['sbatch --parsable --dependency='+env_data['dependency']+' '+filename]
  else:
    order = ['sbatch --parsable '+filename]
  return int(subprocess.check_output(order, shell=True))

