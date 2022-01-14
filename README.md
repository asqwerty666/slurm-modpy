# slurm-modpy
Helper to launch slurm tasks with python scripts

## General Purpose

The use of SLURM tools like *sbatch* is quite easy but tedious. In order to execute a simple order through the schedule manager a script must be built. For repetitive tasks the easiest way is looping the building proccess and change the command to execute as needed. However, every time same directives, other than commands, should be repited, making the code a little unconfortable to read and error prone.

By importing this python functions, a dictionary can previously defined and only the parts that change inside the loop should be redefined any time. Also, I hope the use of dependencies could be as easy as when using *sbatch* directives. In fact the use of a swarm of *sbatch* scripts followed by a warning email job is a lot short when this script is used.

## Description

Only one function is intended to be used here, **send_sbatch()**. This function takes a dictionary as argument with the data to run a given *sbatch* script. The keys of input dictionary should be a subset of:

 - mem\_per\_cpu
 - cpus
 - time
 - job\_name
 - mailtype
 - partition
 - filename
 - output
 - command
 - dependency

Each of these keys corresponds to a directive for *sbatch* and the full set allows us to do a lot of things. The dictionary could be only partially defined. Actually you could use a completely empty dictionary as input. For the missing keys a constructor function is called so defaults values could be loaded. 

The **send_batch()** function generates a script according with the supplied info and launch it. The output of the function is the *job_id* of the launched job, so you could use it to build a dependency for another job or just monitoring it.

## Usage

### Basics

First of all, you need to import the function into your script

```
from slurm import send_sbatch
```

Now you define a dictionary with your desired environment,

```
cdata = {'time':'4:0:0', 'cpus':4, 'job_name':'job_one'}
```

and usually I fill other info inside a loop and launch it,

```
for name in names:
  cdata['filename'] = working_dir+'/'+name+'.sh' # this is the filename of the sbatch script
  cdata['output'] = working_dir+'/'+name+'.out' # this is where the output of the job is stored
  cdata['command'] = 'pdftotext '+name+'.pdf '+name+'.txt' # this is what I want to run in parallel
  send_sbatch(cdata)
```

### Dependencies

Let's say you want to send a warning email after all your jobs finish. Then all you want to do is to define a new dictionary with some basic data and launch it. Must important thing here is that *command* must be not defined.

```
wdata = {'job_name':'job_one', 'filename':working_dir+'warning_end.sh'}
send_sbatch(wdata)
```


## Other info

For other useful info (in spanish): https://detritus.fundacioace.com/wiki/doku.php?id=cluster:slurm.py 
