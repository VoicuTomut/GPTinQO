"""
Code for evaluating answers.
"""

from nltk.translate.ribes_score import sentence_ribes
from nltk.translate.meteor_score import meteor_score
from nltk.translate.nist_score import sentence_nist
from nltk.translate.chrf_score import sentence_chrf
from nltk.translate.gleu_score import sentence_gleu
from bert_score import score as bert_score
from nltk.translate.bleu_score import sentence_bleu
from rouge import Rouge
from pathlib import Path
from openai import OpenAI
from typing import List
import time
from box import Box
from profanity_check import predict, predict_prob
from nltk import sent_tokenize
import nltk
import spacy.cli
import spacy
nltk.download("punkt")
nltk.download("wordnet")





# Define the model name
model_name = "en_core_web_md"

# Check if the model is already installed
if model_name not in spacy.util.get_installed_models():
    # If not installed, download the model
    spacy.cli.download(model_name)

nlp = spacy.load(model_name)


class Sage:
    def __init__(self, model: str, instructions: str, files: List[str]):
        """
        Constructs the gpt sage.
        :param model: what used as a assistant ex: "gpt-3.5-turbo"
        :type model: str
        :param instructions: instructions fot the sage (prompting)
        :type instructions: str
        :param files: list of the files that will be passed to the sage.
        :type files: list
        """
        self.client = OpenAI(api_key="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")
        self.instructions = instructions
        self.model = model
        files = self.upload_files(files)
        # create model
        self.assistant = self.client.beta.assistants.create(
            instructions=self.instructions,
            model=self.model,
            tools=[{"type": "retrieval"}],
            file_ids=[file.id for file in files],
        )
        self.thread = None

    def add_files_to_assistant(self, file_ids: List[str]):
        """
        This function is used to add files like chapter files to the model.
        :param file_ids:
        :type file_ids:list
        :return:
        :rtype:  -
        """
        for file_id in file_ids:
            self.client.assistants.files.create(
                assistant_id=self.assistant.id, file_id=file_id
            )

    def upload_files(self, files: List[Path]):
        """
        Uploads a list of file to the gpt agent
        :param files: list of paths to the files
        :type files: list
        :return: the list of files
        :rtype: list
        """
        files_ = []
        for file in files:
            files_.append(self.upload_file(file))
        return files_

    def upload_file(self, file: Path):
        """
        Upload a file to the gpt.
        :param file: path to the file
        :type file: str
        :return: gpt with the file
        :rtype: -
        """
        with open(file, "rb") as f:
            return self.client.files.create(file=f, purpose="assistants")

    def process_message(self, message):
        """
        Sent a message to the assistant.
        :param message: message content
        :type message: str
        :return: the gpt bot answer
        :rtype: str
        """
        if not self.thread:
            self.thread = self.client.beta.threads.create()

        message = self.client.beta.threads.messages.create(
            thread_id=self.thread.id, role="user", content=message
        )

        run = self.client.beta.threads.runs.create(
            thread_id=self.thread.id,
            assistant_id=self.assistant.id,
            instructions="Please execute the users request.",
        )
        while run.status in ["queued", "in_progress", "cancelling"]:
            time.sleep(1)  # Wait for 1 second
            run = self.client.beta.threads.runs.retrieve(
                thread_id=self.thread.id, run_id=run.id
            )

        if run.status == "completed":
            messages = self.client.beta.threads.messages.list(thread_id=self.thread.id)
            message = messages.data[0].content[0].text.value + "\n"
            return message
        else:
            print(run.status)



class Evaluate:
    def __init__(self, config: Box):
        self.metrics = config.metrics
        self.assistant = Sage(config.model, config.instructions, config.files)
        self.examples = config.examples

    def measure_bert(self, expectation, value):
        # BERTScore
        P, R, F1 = bert_score([expectation], [value], lang="en")
        message = (
            f"BERTScore Precision: {P.item()}, Recall: {R.item()}, F1: {F1.item()},"
        )
        print(message)
        return message

    def measure_nltk(self, expectation, value, measure_func: callable):
        score = measure_func([expectation], value)
        message = f"{measure_func.__name__} Score: {score}"
        print(message)
        return score

    def measure_spacy(
        self,
        expectation,
        value,
    ):
        doc1 = nlp(expectation)
        doc2 = nlp(value)
        similarity = doc1.similarity(doc2)
        print("Similarity:", similarity)
        return similarity

    def measure_profan(self, value):
        message = predict_prob([value])
        message = f"profanity score:{message[0]}"
        print(message)
        return message

    def measure_rogue(self, expectation, value):
        # ROUGE Score
        rouge = Rouge()
        scores = rouge.get_scores(expectation, value)
        rouge_score = scores[0]["rouge-l"]["f"]
        message = f"ROUGE Score: {rouge_score},"
        print(f"ROUGE Score: {rouge_score},")
        return message

    def measure_gpt(self, question, expectation, value):
        prompt = f"Knowing the documentation and the fact that the right answer to the question: '{question}' is target: '{expectation}', evaluate and give a short feedback (20 words) on the following answer: '{value}'. plse respect the ormet from examples : \n ({self.examples}) "
        message = self.assistant.process_message(prompt)
        print(f"GPT Score: {message}")
        message = f"GPT Score: {message}"
        return message

    def measure(self, question, expectation, value):
        performance = {
            "bert_sc": self.measure_bert(expectation, value),
            "rogue": self.measure_rogue(expectation, value),
            "profan": self.measure_profan(value),
            "gpt": self.measure_gpt(question, expectation, value),
            "spacy": self.measure_spacy(expectation, value),
            "blue": self.measure_nltk(expectation, value, sentence_bleu),
            "ribes": self.measure_nltk(expectation, value, sentence_ribes),
            "meteor": self.measure_nltk(
                sent_tokenize(expectation),
                sent_tokenize(value),
                meteor_score,
            ),
            "nist": self.measure_nltk(expectation, value, sentence_nist),
            "chrf": self.measure_nltk(expectation, value, sentence_chrf),
            "gleu": self.measure_nltk(expectation, value, sentence_gleu),

        }

        return performance