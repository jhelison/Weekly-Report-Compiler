# Return all epics were status is work in progress
EPIC_IN_PROGRESS_JQL = 'project = {} and type = Epic and status = "in progress"'

# Return all tasks for a specific EPIC
EPIC_TASKS_JQL = 'parent = {}'