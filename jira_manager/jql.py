# Return all epics were status is work in progress
EPIC_IN_PROGRESS_JQL = (
    'project = {} and type = Epic and status = "in progress" order by cf[{}]'
)

# Return all tasks for a specific EPIC
EPIC_TASKS_JQL = 'parent = {} and status != "Routine" order by created ASC'

# Return tasks for appendix
APPENDIX_TASKS_LIST = 'project = Cayago and issuetype = Epic and key not in ("CAYAG-11", "CAYAG-18", "CAYAG-95", "CAYAG-85", "CAYAG-1", "CAYAG-5", "CAYAG-97") and status != "DONE"  ORDER BY summary'
