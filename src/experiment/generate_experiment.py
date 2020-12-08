"""Generate trials for experiment."""

import os.path as op
import json
import re

from os import listdir

### PATHS
DATA_PATH = "data/raw/stimuli"
SAVE_PATH = "experiment/items.html"



## TODO: Load each file in DATA_PATH, create stimuli
## Should be *two items* for each one. First to require listening, second for response.


## TODO: Remove speakers that we removed from acoustic features analysis. (Should be 18 total...)

## < 24 observations: [10, 12, 13, 14, 15]
## Laptop mic: [16]
## For #23, recording failed: [23]

EXCLUSIONS = [10, 12, 13, 14, 15, 16, 23]
PARTICIPANTS = [ppt for ppt in list(range(1, 26)) if ppt not in EXCLUSIONS]
MODALS = ["window", "temp", "Spanish", "door", "piano", "box"]
DECLARATIVES = ["back", "soup", "car", "laptop", "phone", "office"]

## Path to stimuli (from experimental folder)
STIM_PATH = "../../data/raw/stimuli/"

## Load file names
filenames = [f for f in listdir(DATA_PATH)]
print("Initially {x} files...".format(x = len(filenames)))
filenames.sort(key=lambda f: int(re.sub('\D', '', f)))
## Remove participants
filenames = [f for f in filenames if int(f.split("_")[0]) in PARTICIPANTS]
print("After excluding participants: {x} files.".format(x = len(filenames)))



## TODO: Redo this, chunk by speaker --> so have a bunch of nested trials for each speaker
## TODO: Sort filenames

doc = ''
topics = []
for f in filenames:

	trial_names = []

	speaker, intent, topic = f.replace(".wav", "").split("_")
	topics.append(topic)

	# Determine form
	if topic in DECLARATIVES:
		form = "non-conventional"
	elif topic in MODALS:
		form = "conventional"
	else:
		raise Exception("Topic not found")

	## TODO: Categorize "form"


	struct_initial = {
		'type': 'audio-button-response',
		'choices': [],
		'data': {'condition': intent, 'topic': topic, 'speaker': speaker, 'form': form},
		'stimulus': op.join(STIM_PATH, f),
		'prompt': "<br><p>Is this person making a request?</p>",
		'trial_ends_after_audio': True
	}

	struct_response = {
		'type': 'html-button-response',
		'choices': ['Yes', 'No'],
		'stimulus': '',
		'data': {'condition': intent, 'topic': topic, 'speaker': speaker, 'form': form},
		'prompt': "<p>Is this person making a request?</p>",
		'response_ends_trial': True
	}

	nested_trial = {'timeline': [struct_initial, struct_response]}

	trial_name = 's_{speaker}_{topic}_{intent}_trial'.format(speaker=speaker, topic=topic, intent=intent)
	trial_names.append(trial_name)

	doc += 'var {tn} = '.format(tn=trial_name) + json.dumps(nested_trial, indent=4) + "\n\n"


# doc += 'all_trials = ' + json.dumps(multi_array, indent=4) + "\n\n"

## TODO: Now create each speaker block

for speaker in PARTICIPANTS:
	s_declarative_trials = []
	for topic in DECLARATIVES:
		for intent in ['request', 'statement']:
			trial_name = 's_{speaker}_{topic}_{intent}_trial'.format(speaker=speaker, topic=topic, intent=intent)
			s_declarative_trials.append(trial_name)

	s_modal_trials = []
	for topic in MODALS:
		for intent in ['request', 'question']:
			trial_name = 's_{speaker}_{topic}_{intent}_trial'.format(speaker=speaker, topic=topic, intent=intent)
			s_modal_trials.append(trial_name)

	s_declarative_trials_timeline = {'timeline': s_declarative_trials}		
	s_modal_trials_timeline = {'timeline': s_modal_trials}

	doc += 'var s_{speaker}_declaratives = '.format(speaker=speaker) + json.dumps(s_declarative_trials_timeline, indent=4) + "\n\n"
	doc += 'var s_{speaker}_modals = '.format(speaker=speaker) + json.dumps(s_modal_trials_timeline, indent=4) + "\n\n"


## Create declarative blocks
declarative_blocks = ["s_{speaker}_declaratives".format(speaker=speaker) for speaker in PARTICIPANTS]
doc += 'var declarative_blocks = ' + json.dumps(declarative_blocks, indent=4) + "\n\n"

## Create modal blocks
modal_blocks = ["s_{speaker}_modals".format(speaker=speaker) for speaker in PARTICIPANTS]
doc += 'var modal_blocks = ' + json.dumps(modal_blocks, indent=4) + "\n\n"

with open(SAVE_PATH, "w") as f:
	f.write(doc)




