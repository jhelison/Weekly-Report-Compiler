# Jira - Gdocs: Weekly Report Compiler

This project is a utility for working with Google Docs and Jira integration. It provides functionality to automate tasks related to managing and formatting content in Google Docs based on data from Jira.

## Table of Contents

-   [Introduction](#introduction)
-   [Features](#features)
-   [Installation](#installation)
-   [Usage](#usage)
-   [Contributing](#contributing)
-   [License](#license)

## Introduction

The Google Docs and Jira integration utility simplifies the process of working with Jira data in Google Docs. It offers features for automating tasks such as replacing tags with Jira data, creating tables, formatting text, and more. This utility aims to streamline the workflow and enhance productivity when working with Jira and Google Docs together.

## Features

-   Replace tags in Google Docs with Jira data.
-   Create tables with data fetched from Jira.
-   Format text using Markdown syntax and clean Jira Markdown.
-   Apply date chips and worked tasks tables to Google Docs.
-   Automatically generate Jira-based reports in Google Docs.

## Installation

To use this utility, follow these steps:

1. Clone the repository: `git clone git@github.com:jhelison/Weekly-Report-Compiler.git`
2. Install pyenv for managing Python versions. Refer to the [pyenv documentation](https://github.com/pyenv/pyenv#installation) for installation instructions specific to your operating system.
3. Install the required Python version for your project using pyenv. Run the following command in the project's root directory:

```shell
pyenv install 3.10
```

4. Create a virtual environment for the project using pyenv. Run the following command:

```shell
pyenv virtualenv 3.10 <env-name>
```

Replace <env-name> with a name for your virtual environment.

5. Activate the virtual environment:

```shell
pyenv activate <env-name>
```

6. Install the required dependencies using pip:

```shell
pip install -r requirements.txt
```

7. Copy the .env.example file to .env:

```shell
cp .env.example .env
```

8. Edit the .env file and provide values for the following environment variables:

-   `JIRA_EMAIL`: The email address associated with your Jira account.
-   `JIRA_TOKEN`: The API token or password for your Jira account.
-   `JIRA_SERVER`: The URL of your Jira server.
-   `GOOGLE_CRED_FILE`: The path to your Google API credentials JSON file.
-   `GOOGLE_TOKEN`: The path to your Google API token JSON file.
-   `CONFIG_FILE`: The path to your configuration file (e.g., ./config.toml).

Note: The environment variables mentioned above are necessary for the utility to authenticate and connect to Jira and Google Docs. Ensure that you have the required credentials and permissions for accessing the respective services.

### Creating Jira custom fields

1. Log in to your Jira account and navigate to your desired Jira project.
2. Click on the "Settings" option in the left-hand sidebar.
3. In the Project Settings menu, select "Screens" from the "Issue Features" section.
4. On the Screens page, click on the "Custom Fields" tab.
5. Click on the "Add Custom Field" button to create a new custom field.
6. Choose the type of custom field that matches your requirements. For example, if you need a text field, select "Text Field (single line)".
7. Configure the details of the custom field, such as the name, description, and field options.
8. Save the custom field by clicking the "Create" or "Save" button.

Repeat the above steps for each custom field mentioned in your configuration file.

Ensure that you note down the custom field IDs assigned to each custom field you create. These IDs will be used to configure the application later.

Once you have created the custom fields in Jira and obtained their IDs, update the corresponding values in your configuration file (config.toml) under the [jira] section:

-   `task_weekly_report_field`: Update this field with the custom field ID for the task weekly report field.
-   `epic_weekly_report_field`: Update this field with the custom field ID for the epic weekly report field.
-   `epic_order_field`: Update this field with the custom field ID for the epic order field.

Save the configuration file after making the necessary updates.

These custom fields will be used by the application to fetch the required data from Jira for generating the weekly report.

Please note that the exact steps to create custom fields may vary depending on your Jira version and configuration. Refer to the Jira documentation or contact your Jira administrator for further assistance if needed.

Include these instructions in your README, preferably in the "Setting Up Custom Fields in Jira" section.

## Usage

To use the utility, you need to provide the necessary configurations and credentials for Jira and Google Docs. This includes setting up environment variables and configuration files.

Configure the utility by editing the `config.toml` file located in the project's root directory. The file contains various sections for configuring Jira and Google Docs integration, as well as style settings. Modify the values as per your project's requirements. Here's an example of the config.toml file:

```toml
[jira]
# Jira configuration
project = <project-name>
task_weekly_report_field = <weekly_report_field>
epic_weekly_report_field = <weekly_report_field>
epic_order_field = <epic_order_field>

[jira.jql]
# JQL Jira configuration
epic_in_progress = 'project = {} and type = Epic and status = "in progress" order by cf[{}]'
epic_tasks = 'parent = {} and status != "Routine" order by created ASC'
appendix_task_list = 'project = Cayago and issuetype = Epic and status != "DONE"  ORDER BY summary'

[doc]
# Google doc configuration
document_id = <document_id>
start_date = <document_start_date>
end_date = <document_end_date>

[style]

[style.colors]
# Styles for the text

[style.table]
```

Fill in the following values in the config.toml file:

-   `project`: Specify the name of your Jira project.
-   `task_weekly_report_field`: Provide the field ID or name for the weekly report field associated with tasks in Jira.
-   `epic_weekly_report_field`: Provide the field ID or name for the weekly report field associated with epics in Jira.
-   `epic_order_field`: Provide the field ID or name for the order field associated with epics in Jira.
-   `document_id`: Specify the ID of your Google Docs document. You can find the ID in the URL of the document.
-   `start_date`: Specify the start date for your document in the format "YYYY-MM-DD".
-   `end_date`: Specify the end date for your document in the format "YYYY-MM-DD".

To run the compiler use:

```shell
python main.py
```

### Adding Tags to the Document

To generate the desired content in your Google Docs document, you need to add specific tags at appropriate locations. The utility will identify these tags and replace them with the generated content. Here are the tags you should add:

-   `<start_date_small>`: Replace this tag with the formatted start date in small size.
-   `<start_date_big>`: Replace this tag with the formatted start date in big size.
-   `<end_date_small>`: Replace this tag with the formatted end date in small size.
-   `<end_date_big>`: Replace this tag with the formatted end date in big size.
-   `<worked_tasks_table>`: Place this tag where you want the worked tasks table to be inserted.
-   `<worked_tasks_list>`: Place this tag where you want the worked tasks list to be inserted.
-   `<appendix_tasks_list>`: Place this tag where you want the appendix tasks list to be inserted.

Ensure that you add the tags exactly as mentioned above, including the angle brackets (\< and \>).

Once you've added the tags, run the utility as described in the previous section. The utility will process the document, replace the tags with the generated content, and create a final report.

Make sure to review the generated document to verify that the content and formatting meet your requirements. Adjust the tags' placement and formatting in the document if necessary.

## Contributing

Contributions to this project are welcome! If you find any issues or have ideas for improvements, please submit them through the issue tracker or open a pull request. Make sure to follow the contribution guidelines provided in the project's repository.
