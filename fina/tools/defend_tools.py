from typing import Optional, Dict, Any
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Simple module-level cache so repeated calls reuse the loaded model/tokenizer
_TOKENIZER: Optional[AutoTokenizer] = None
_MODEL: Optional[AutoModelForSequenceClassification] = None


def _load_model_and_tokenizer(model_name: str):
	"""Load and cache the tokenizer and model for the given model_name.

	Returns (tokenizer, model).
	"""
	global _TOKENIZER, _MODEL
	if _TOKENIZER is None or _MODEL is None:
		_TOKENIZER = AutoTokenizer.from_pretrained(model_name)
		_MODEL = AutoModelForSequenceClassification.from_pretrained(model_name)
	return _TOKENIZER, _MODEL


def classify_prompt_safety(
	text: str,
	model_name: str = "Mustartoo/defend-model-v1",
	max_length: int = 512,
) -> int:
	"""
	Classify whether `text` is malicious (policy-violating) or benign using a
	sequence-classification model.

	Returns a dictionary with keys:
	  - label: str (human-friendly label, derived from model.config.id2label when available)
	  - class_id: int (predicted class index)
	  - scores: list[float] (softmax probabilities for each class)

	Notes:
	  - The function caches the tokenizer and model at module level so repeated
		calls don't re-download or re-instantiate the model.
	  - The function runs inference in eval mode under torch.no_grad().
	"""
	tokenizer, model = _load_model_and_tokenizer(model_name)

	device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
	model.to(device)
	model.eval()

	inputs = tokenizer(text, truncation=True, max_length=max_length, return_tensors="pt")
	# move tensors to device
	inputs = {k: v.to(device) for k, v in inputs.items()}

	with torch.no_grad():
		outputs = model(**inputs)

	logits = outputs.logits
	pred = int(torch.argmax(logits, dim=-1).item())

	# Determine a human-readable label from model config if available
	label = None
	try:
		id2label = getattr(model.config, "id2label", None)
		if id2label:
			# id2label keys may be strings or ints
			label = id2label.get(pred) if isinstance(id2label, dict) else None
	except Exception:
		label = None

	if label is None:
		# fallback mapping commonly used: 0 -> Benign, 1 -> Malicious
		label = "Malicious" if pred == 1 else "Benign"

	return pred

