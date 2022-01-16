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


