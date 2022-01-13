# slurm-modpy
Helper to launch slurm tasks with python scripts

## General Purpose

The use of SLURM tools like **sbatch** is quite easy but tedious. In order to execute a simple order through the schedule manager a script must be built. For repetitive tasks the easiest way is looping the building proccess and change the command to execute as needed. However, every time same directives, other than commands, should be repited, making the code a little unconfortable to read and error prone.

By importing this python functions, a dictionary can previously defined and only the parts that change inside the loop should be redefined any time. Also, I hope the use of dependencies could be as easy as when using **sbatch** directives. In fact the use of a swarm of **sbatch** scripts followed by a warning email job is a lot short when this script is used.

## Description

Only one function is intended to be used here, **send_sbatch()**. 

## Usage

## Other info

See (in spanish), for other usefull info: https://detritus.fundacioace.com/wiki/doku.php?id=cluster:slurm.py 
