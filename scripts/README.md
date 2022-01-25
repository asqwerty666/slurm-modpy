# example scripts

Here you can find some scripts that show how to use the helper

### slurm\_list.py

The script reads a file with a list of orders and executes them with the same priority

```
$ ./slurm_list.py my_orders.list
```

where *my\_orders.list* is a file containing a single lsit of orders, like,

```
cp file1 file2
grep "huhuh" file2 > file3
whatever_i_want
```

### slurm\_list\_deps.py

This new scripts also reads a file with a list of orders but with dependencies. That is, the file
*my\_orders.list* should be formated as,

```
1:cp file1 file2
2:grep "huhuh" file2 > file3
1:whatever_i_want
```

where the first number shows the job precedence, meaning that the *grep* command should be executed only after the *cp* commands finish. However the last command is not related to anything and is executed at the same time than the first one.
