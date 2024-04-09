from pathlib import Path
from openai import OpenAI
from typing import List
import time

client = OpenAI()


def upload_file(file_path: Path):
    with open(file_path, "rb") as f:
        client.files.create(file=f, purpose="assistants")


def list_files():
    return client.files.list()


def list_file_ids():
    return [file.id for file in list_files()]


def create_assistant(file_ids: List[str]):
    # Add the file to the assistant
    return client.beta.assistants.create(
        instructions="You are a customer support chatbot. Use your knowledge base to best respond to customer queries.",
        model="gpt-3.5-turbo",
        tools=[{"type": "retrieval"}],
        file_ids=file_ids,
    )


def upload_files_from_enciclopedy():
    for file in Path(
        "/Users/raul-ioandragoiu/projects/proiect_qq/softmind/data/enciclopedia"
    ).iterdir():
        upload_file(file)


def add_files_to_assistant(assistant_id: str, file_ids: List[str]):
    for file_id in file_ids:
        client.beta.assistants.files.create(assistant_id=assistant_id, file_id=file_id)


def run_one_message(message: str, assistant, thread):
    message = client.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=message
    )

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
        instructions="Please execute the users request.",
    )
    while run.status in ["queued", "in_progress", "cancelling"]:
        time.sleep(1)  # Wait for 1 second
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

    if run.status == "completed":
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        print(messages.data[0].content[0].text.value + "\n")
    else:
        print(run.status)


def run_assistant():
    assistant = client.beta.assistants.retrieve("asst_b69jTsH9XK6Nved0xVOmNxOj")
    thread = client.beta.threads.create()
    run_one_message(
        "Select a chapter and generate one specific question based on it.",
        assistant=assistant,
        thread=thread,
    )
    run_one_message("Answer the question", assistant=assistant, thread=thread)
    run_one_message(
        "Give feedback to the answer and suggest some improvements.",
        assistant=assistant,
        thread=thread,
    )

