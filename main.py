import asyncio, time, json, os
from claude_agent_sdk import query, ClaudeAgentOptions

def hours_minutes_seconds(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return int(hours), int(minutes), int(secs)

def change_working_directory(path):
    # Get and print the current working directory
    cwd = os.getcwd()
    print(f"Current working directory: {cwd}")

    try:
        os.chdir(path)
        print(f"Working directory changed to: {os.getcwd()}")
    except FileNotFoundError:
        print(f"Directory: {new_directory} does not exist")
    except PermissionError:
        print(f"No permissions to access {new_directory}")

async def main():
    # Load instructions from JSON file
    instructions = json.load(open("instructions.json") )

    # Change to the specified working directory
    change_working_directory(instructions["folder_path"])

    # Process each task in the instructions
    for task in instructions["tasks"]:
        if 'name' in task:
            print(f"Task: {task['name']}")
        
        start_time = time.time() 
        local_start_time = time.ctime()
        print("Starting task. Time is:", local_start_time)

        # Construct the query prompt with branch creation instructions
        query_prompt = f"""
        {task['prompt']}

        Any suggested plans are automatically approved.

        For Database changes, ensure to include a SQL .txt file containing the queries that can be run to apply those changes.

        Create a Git branch named "{task['branch']}" before making any file changes, then after making changes 
        commit them, and finally push to the {task['branch']} branch.
        """

        options = ClaudeAgentOptions(
            # allowed_tools=["Read", "Write", "Edit", "Bash", "Glob", "Grep", "WebSearch", "WebFetch"],
            permission_mode="bypassPermissions", # you can adjust permissions as needed
        )

        # Execute the query using Claude Agent SDK
        async for message in query(prompt=query_prompt, options=options):
            if hasattr(message, "result"):
                print(message.result)

        end_time = time.time()
        local_end_time = time.ctime()
        elapsed_time_seconds = end_time - start_time
        h, m, s = hours_minutes_seconds(elapsed_time_seconds)
        print("Task completed. Time is:", local_end_time)
        print("Elapsed time (h:m:s):", f"{h}h:{m}m:{s}s")

        # Wait for the specified interval before starting the next task
        print(f"Waiting for {instructions['interval_mins']} minutes before next task...")
        time.sleep(int(instructions["interval_mins"]) * 60)

    completion_time = time.time()
    local_completion_time = time.ctime()
    print("All tasks completed. Time is:", local_completion_time)


asyncio.run(main())