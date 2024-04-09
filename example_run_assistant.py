from gpt_sage.assistant import Evaluate
from gpt_sage.config import get_config
import time
import json

GPT_CONFIG = "config/gpt.toml"
REQUEST_STORAGE = "data/request_data/history.json"

config = get_config(GPT_CONFIG)
judge = Evaluate(config)

u_id = "user_id"
question = "Why is superposition important for quantum computing?"
expectation = "Entanglement is crucial for quantum computing because it enables complex computations and correlations that are impossible in classical computings"
value = "Entanglement enables parallel processing, gate operations, error correction, quantum teleportation, and superposition, crucial for quantum computing's power and functionality."
performance = judge.measure(question, expectation, value)
print(performance)

