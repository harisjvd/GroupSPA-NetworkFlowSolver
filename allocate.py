"""
Script for student assignment based on preferences using network flow optimization.
"""

import networkx as nx
import pandas as pd
from collections import defaultdict

def redistribute_students(topics, topic_group_count, students, min_group_size, max_group_size):
  """
    Redistribute students among groups based on their preferences.
  """

  # Combine groups for each topic and store students for redistribution
  students_to_redistribute = []
  for t in topics:
      combined_group = [student for group in topic_group_count[t] for student in group]
      topic_group_count[t] = []
      #Split the combined group into groups of size min_group_size to max_group_size
      while len(combined_group) >= min_group_size:
          group_size = min(len(combined_group), max_group_size)
          new_group = combined_group[:group_size]
          combined_group = combined_group[group_size:]
          topic_group_count[t].append(new_group)

      if combined_group:
          students_to_redistribute.extend(combined_group)

  # Redistribute students
  while students_to_redistribute:
      s = students_to_redistribute.pop(0)
      prefs = students[s]
      assigned = False
      for t in prefs:  # Checking all preferences in order
          if topic_group_count[t] and len(topic_group_count[t][-1]) < max_group_size and sum(len(group) for group in topic_group_count[t]) + 1 <= topic_use_limit * max_group_size:
              topic_group_count[t][-1].append(s)
              assigned = True
              break
      if not assigned:  # If no preference could be fulfilled, assign randomly
          for t in topics:
              if not topic_group_count[t]:
                  topic_group_count[t].append([s])
                  assigned = True
                  break
              elif len(topic_group_count[t][-1]) < max_group_size and sum(len(group) for group in topic_group_count[t]) + 1 <= topic_use_limit * max_group_size:
                  topic_group_count[t][-1].append(s)
                  assigned = True
                  break
      if not assigned:
          print(f"Unable to assign student {s} to any topic")

  #Merge small groups to form groups of at least min_group_size
  for t in topics:
      for i, group in enumerate(topic_group_count[t]):
          if len(group) < min_group_size:
              next_group = topic_group_count[t][i + 1] if i + 1 < len(topic_group_count[t]) else None
              while len(group) < min_group_size and next_group and next_group[-1]:
                  group.append(next_group.pop())
                  if not next_group:
                      topic_group_count[t].pop(i + 1)

  #Combine small groups to reach min_group_size
  small_groups = [group for t in topics for group in topic_group_count[t] if len(group) < min_group_size]
  while small_groups:
    group = small_groups.pop(0)
    for t in topics:
      while len(group) < min_group_size and topic_group_count[t] and len(topic_group_count[t][-1]) > min_group_size:
        group.append(topic_group_count[t][-1].pop())
        if len(topic_group_count[t][-1]) == min_group_size:
          break
      if len(group) == min_group_size:
          break

def assignment_count(students, topic_group_count):
    """
    Count the number of students assigned to their respective preferences.
    """
    scores = {'first': 0, 'second': 0, 'third': 0, 'fourth': 0, 'random': 0}
    for t in topics:
      for group in topic_group_count[t]:
        for s in group:
          prefs = students[s]
          if t == prefs[0]:
            scores['first'] += 1
          elif len(prefs) > 1 and t == prefs[1]:
            scores['second'] += 1
          elif len(prefs) > 2 and t == prefs[2]:
            scores['third'] += 1
          elif len(prefs) > 3 and t == prefs[3]:
            scores['fourth'] += 1
          else:
            scores['random'] += 1

    total  = (scores['first'] + scores['second'] + scores['third']+ scores['fourth'])
    return scores, total


def result_file():
  """
    Save the student assignment results to a CSV file.
  """
  result_data = []
  total_assigned = 0
  for t in topics:
      for i, group in enumerate(topic_group_count[t]):
          total_assigned += len(group)
          for student in group:
              result_data.append({"topic": t, "group": i + 1, "student": student})

  result_df = pd.DataFrame(result_data)
  result_df.to_csv("allocation.csv", index=False)
  return total_assigned


def log_file():
  """
    Log the results and parameters into a text file.
  """
  with open('log_file.txt', 'w') as log_file:
    assigned_topics = sum(1 for topic_groups in topic_group_count.values() if topic_groups)
    if total_assigned == len(students):
      log_file.write(f"All {total_assigned} students were assigned successfully.\n")
    else:
        log_file.write(f"Assigned {total_assigned} out of {len(students)} students.\n")
    log_file.write(f"Assigned topics: {assigned_topics} out of {len(topics)}.\n\n")
    log_file.write("\nParameters:\n")
    log_file.write(f"Min group size {min_group_size}\n")
    log_file.write(f"Max group size: {max_group_size}\n")
    log_file.write(f"Topic use limit: {topic_use_limit}\n")
    log_file.write("\nAssignment Summary:\n")
    log_file.write(f"Total assigned with preferences: {total}\n")
    log_file.write(f"Total assigned at random: {assigned_counts['random']}\n\n")
    log_file.write("Score Function:\n")
    log_file.write(f"  1st preference: {assigned_counts['first']}\n")
    log_file.write(f"  2nd preference: {assigned_counts['second']}\n")
    log_file.write(f"  3rd preference: {assigned_counts['third']}\n")
    log_file.write(f"  4th preference: {assigned_counts['fourth']}\n")


def main():
  ## Parameters
  min_group_size = 4
  max_group_size = 5
  topic_use_limit = 7
  students_df = pd.read_csv('student-data1.csv')

  ## Extracting student data
  students = {}
  for row in students_df.itertuples():
      student_id = row[1]
      prefs = [p for p in row[2:] if pd.notnull(p) and p != 0]  #Considers only students with exactly four preferences
      if prefs:
          students[student_id] = prefs


  ## Extracting list of topics
  topics = set()
  for _, row in students_df.iterrows():
      for topic in row[1:]:
          if not pd.isnull(topic) and topic != 0:
              topics.add(int(topic))
  topics = sorted(list(topics))

  ## Initialize directed graph (network)
  G = nx.DiGraph()
  G.add_node("source")
  G.add_node("sink")
  #Add nodes for students and topics
  for s in students:
      G.add_node(s)
  for t in topics:
      G.add_node(t)
  #Add edges between source and students (capacity 1)
  for s in students:
      G.add_edge("source", s, capacity=1)
  #Add edges between students and topics (capacity 1, weight based on preference)
  for s in students:
      prefs = students[s]
      for i, t in enumerate(prefs):
          G.add_edge(s, t, capacity=1, weight=i)
  #Add edges between topics and sink (capacity based on max_group_size and topic_use_limit)
  for t in topics:
      G.add_edge(t, "sink", capacity=max_group_size * topic_use_limit, weight=0)

  #Compute minimum cost flow
  flow_dict = nx.max_flow_min_cost(G, "source", "sink")


  #Process flow results & create initial topic groups
  topic_group_count = defaultdict(list)
  for t in topics:
      assigned_students = []
      for s in students.keys():
          if s in flow_dict and t in flow_dict[s] and flow_dict[s][t] > 0:
              assigned_students.append(s)
              if len(assigned_students) == max_group_size:
                  topic_group_count[t].append(assigned_students)
                  assigned_students = []

      if assigned_students:
          topic_group_count[t].append(assigned_students)


  redistribute_students(topics, topic_group_count, students, min_group_size, max_group_size)
  total_assigned = result_file()
  assigned_counts, total = assignment_count(students, topic_group_count)
  log_file()

if __name__ == "__main__":
    main()