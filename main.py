from dotenv import load_dotenv
from config.config import get_config
from jira_manager.epic import epic_in_progress_tasks
from gdocs.handlers import handle_tags

if __name__ == "__main__":
    load_dotenv()
    config = get_config()
    handle_tags(config)
