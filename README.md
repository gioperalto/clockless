# Clockless

A task automation tool that uses the Claude Agent SDK to process coding tasks sequentially. Define a list of tasks in a configuration file, and Clockless will execute each one using Claude, automatically creating git branches, committing changes, and pushing to remote.

## Features

- Process multiple coding tasks from a JSON configuration file
- Automatic git branch creation, commits, and pushes for each task
- Configurable intervals between tasks
- Timing reports for each task

## Setup

### 1. Create a Python virtual environment

```bash
python -m venv venv
```

### 2. Activate the virtual environment

On macOS/Linux:
```bash
source venv/bin/activate
```

On Windows:
```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` and add your Anthropic API key:

```
ANTHROPIC_API_KEY=your-actual-api-key
```

## Configuration

Create an `instructions.json` file based on the provided example:

```bash
cp instructions.json.example instructions.json
```

Edit `instructions.json` with your tasks:

```json
{
  "folder_path": "path/to/your/project",
  "interval_mins": 5,
  "tasks": [
    {
      "name": "Feature name",
      "branch": "feature-branch",
      "prompt": "Description of the task for Claude to complete"
    }
  ]
}
```

### Configuration options

| Field | Description |
|-------|-------------|
| `folder_path` | Path to the project directory where tasks will be executed |
| `interval_mins` | Minutes to wait after each task before starting the next |
| `tasks` | Array of task objects |
| `tasks[].name` | (Optional) Display name for the task |
| `tasks[].branch` | Git branch name to create for this task |
| `tasks[].prompt` | The prompt describing what Claude should do |

## Usage

Run the tool:

```bash
python main.py
```

Clockless will:
1. Read your `instructions.json` configuration
2. Change to the specified project directory
3. For each task:
   - Create a new git branch
   - Execute the task using Claude
   - Commit and push changes
   - Wait for the specified interval before the next task
