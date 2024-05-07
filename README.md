#

## Flowchart for Jupyter Notebook File Compression and Status Logging

```mermaid
flowchart TD

A(START) --> B{Condition 1}

B --> |False| C[Statement 1]

B --> |True| D{Condition 2}

D --> |True| E[Statement 2]

E --> F{Condition 3}

D --> |False| F{Condition 3}

F --> |True| G[Statement 3]
```


> Condition 1: Check whether there exists a record for all Jupyter Notebook files in the current directory.
>
> Statement 1: If Condition 1 is False, create a record for all Jupyter Notebook files in the current directory immediately, while generating the corresponding pre-compressed copy for each file as well as compressing any copies that exceed the preset size limit.
>
> Condition 2: If Condition 1 is True, read this record and check whether there are certain entries in this record for which the corresponding Jupyter Notebook file cannot be found.
>
> Statement 2: If Condition 2 is True, delete these entries and eventually reset the index.
>
> Condition 3: Regardless of whether Condition 2 is True or False, check whether there are any Jupyter Notebook files in the current directory that do not have a corresponding entry in this record.
>
> Statement 3: If condition 3 is True, the information relating to the file will be added to the record as the most recent entry, and its corresponding indexes will be recorded separately in a list of indexes dedicated to recording altered or newly added entries.



