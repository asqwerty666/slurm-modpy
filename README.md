# slurm-modpy
Helper to launch [slurm](https://slurm.schedmd.com/) tasks within python scripts

## General Purpose

The use of SLURM tools like *sbatch* is quite easy but tedious. In order to execute a simple order through the schedule manager a script must be built. For repetitive tasks the easiest way is looping the building proccess and change the command to execute as needed. However, every time same directives, other than commands, should be repeated, making the code a little unconfortable to read and error prone.

By importing this python functions, a dictionary can previously defined and only the parts that change inside the loop should be redefined any time. Also, I hope the use of dependencies could be as easy as when using *sbatch* directives. In fact the use of a swarm of *sbatch* scripts followed by a warning email job is a lot short when this script is used.

This was built intentionaly avoiding the object oriented programming thinking in,

  1. Give to absolute begginers, on both python and slurm, the possibility of messing with the code
  2. This should be a door to cluster programming so you should really think what you want

## Description

Only one function is intended to be used here, **send_sbatch()**. This function takes a dictionary as argument with the data to run a given *sbatch* script. The keys of input dictionary should be a subset of:

 - mem\_cpu
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

Aditionally, if the input dictionary include a **True** value for the key *test*, the slurm scripts are wrote to disk but not executed. Note that the default value for testing is **False**.

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

and ussually I fill other info inside a loop and launch it,

```
for name in names:
  cdata['filename'] = working_dir+'/'+name+'.sh' # this is the filename of the sbatch script
  cdata['output'] = working_dir+'/'+name+'.out' # this is where the output of the job is stored
  cdata['command'] = 'pdftotext '+name+'.pdf '+name+'.txt' # this is what I want to run in parallel
  send_sbatch(cdata)
```

Also, as explained before, the code,

```
cdata['test'] = 1
send_sbatch(cdata)
``` 

write the slurm script to disk but don't send them to the queue. This way we can easily switch from testing to production by only asigning a **False** value under the *test* key (or erasing it!). That is,

```
cdata['test'] = 0
send_sbatch(cdata)
```

will ignore the *test* key and will send the slurm scripts to the queue.

### Dependencies

Let's say you want to send a warning email after all your jobs finish. Then all you want to do is to define a new dictionary with some basic data and launch it. Must important thing here is that *command* must be not defined.

```
wdata = {'job_name':'job_one', 'filename':working_dir+'warning_end.sh', 'dependency':'singleton'}
send_sbatch(wdata)
```
Notice that if no *command* is especified the *sbatch* will do nothing but send an email at the end. 

But in general, the dependencies mechanism of slurm brings a very rich dynamics that can be used here. By example,

``` 
p = send_sbatch(cdata)
cdata2['dependency'] = 'afterok:'+str(p)
send_sbatch(cdata2)
```

will execute the second *sbatch* script after the finalization of the first one. Or you can send some scripts and execute another one after them,

```
pids = []
p = send_sbatch(cdata1)
pids.append(p)
p = send_sbatch(cdata2)
pids.append(p)
...
deps = ','.join(map(str,pids))
cdata_end['dependency'] = 'afterok:'+deps
send_sbatch(cdata_end)
```

## Other info
 
 - [sbatch manpage](https://slurm.schedmd.com/sbatch.html)


## Related (and highly superior) projects

 - [simple\_slurm](https://github.com/amq92/simple_slurm)

