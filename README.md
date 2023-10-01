# GroupSPA-NetworkFlowSolver

This code provides a solution to the Group Student-Project Allocation (Group-SPA) problem. It involves allocating students to project topics based on their ranked preferences while adhering to certain constraints like group size and topic use limits.

## Overview

The solution is based on creating a flow network to model the allocation problem. It then computes the maximum flow with minimum cost to determine the best allocation of students to topics.

## Imports

```python
import networkx as nx
import pandas as pd
import random
from collections import defaultdict
```

## Parameters
- min_group_size: Minimum size of a student group.
- max_group_size: Maximum size of a student group.
- topic_use_limit: The maximum number of groups a topic can be assigned to.
- students_df: DataFrame containing students and their topic preferences.

```python
min_group_size = 6
max_group_size = 7
topic_use_limit = 2
students_df = pd.read_csv('Preferences2.csv')
```

## Input
The program expects a CSV file Preferences2.csv with student IDs followed by their ranked topic preferences.

Example format:
```python
StudentID,Preference1,Preference2,Preference3,Preference4
101,3,2,1,4
102,2,1,3,4
...
```

## Output
- allocation.csv: A file with the allocated groups. Columns include the topic, group number, and student.
- log_file.txt: Contains logs about the allocation results and score function.
  
## Functions
`Main Flow Computation`
This section constructs the directed graph, adds nodes for students and topics, and establishes the necessary connections (edges). It computes the flow to determine the initial student-topic allocation.

`redistribute_students(...)`
This function takes care of redistributing students among the topics, ensuring that the group size constraints are met and no student is left unassigned.

`assignment_count(...)`
Quantifies the quality of the assignment by counting the number of students assigned to their 1st, 2nd, 3rd, and 4th preferences or those assigned randomly.

`result_file()`
Writes the allocation results to a CSV file.

`log_file()`
Writes a summary of the allocation and the score function results to a text file.

## Execution
After setting the parameters and reading the input data, the script processes the data to determine the allocations and then redistributes students as needed. Finally, the allocation results and log details are written to their respective output files.

## Acknowledgments
I would like to extend my sincere gratitude to Professor Thomas Erlebach for his invaluable guidance and support throughout this research. His feedback and insights have been instrumental in shaping this project.

