"""Extract features from audio files."""

import os 

import numpy as np
import pandas as pd
import parselmouth

from scipy.stats import linregress
from tqdm import tqdm


## Item numbers
topic_to_stimNum = {'car': 1,
					'back': 2,
					'box': 3,
					'door': 4,
					'laptop': 5,
					'office': 6,
					'phone': 7,
					'piano': 8,
					'soup': 9,
					'spanish': 10,
					'window': 11,
					'temperature': 12}


def extract_features(f0, name="f0", window=3):
	"""Extract features from component, e.g. f0 or intensity."""
	slope_f0 = linregress(list(range(len(f0))), f0).slope

	return {'mean_{name}'.format(name=name): np.mean(f0),
			'range_{name}'.format(name=name): max(f0) - min(f0),
			'sd_{name}'.format(name=name): np.std(f0),
			'slope_{name}'.format(name=name): slope_f0,
			'duration_{name}'.format(name=name): len(f0)}


def extract_intensity_features(f0, name="f0", window=3):
	"""Extract features from component, e.g. f0 or intensity."""
	slope_f0 = linregress(list(range(len(f0))), f0).slope

	return {'mean_{name}'.format(name=name): np.mean(f0),
			'sd_{name}'.format(name=name): np.std(f0)}

def extract_file_features(filepath):
	"""Extract acoustic features from sound file."""

	snd = parselmouth.Sound(filepath)

	# Get pitch features
	pitch = snd.to_pitch()
	pitch_values = pitch.selected_array['frequency']
	og_duration = len(pitch_values)
	pitch_values = [i for i in pitch_values if i > 0]
	features = extract_features(pitch_values, name="f0")

	# Get intensity features
	intensity = snd.to_intensity()
	intensity_values = intensity.values[0]
	features.update(extract_intensity_features(intensity_values, name="intensity"))

	# Get true label (intent) and speaker
	if "original_stimuli" in filepath:
		filename = filepath.split("/")[-1].split(".")[0]
		file_features = filename.split("_")
		label, topic = file_features[0:2]
		speaker = filepath.split("/")[3]

		# ppt, label, topic = filename.split("_")
		# features['ppt_id'] = ppt
		features['label'] = label.lower()
		features['intent'] = label.lower()
		features['speaker'] = speaker
	else:
		filename = filepath.split("/")[-1].split(".")[0]
		file_features = filename.split("_")
		ppt, label, topic = file_features[0:3]
		# ppt, label, topic = filename.split("_")
		features['ppt_id'] = ppt
		features['label'] = label
		features['intent'] = label
		features['speaker'] = ppt

	# recode topic
	if topic == "temp":
		topic = "temperature"
	features['topic'] = topic.lower()

	features['stimNum'] = topic_to_stimNum[features['topic']]

	# Determine form
	if features['topic'] in ["back", "soup", "car", "laptop", "phone", "office"]:
		features['form'] = "non-conventional"
	else:
		features['form'] = "conventional"

	return features


def main(dataset):
	"""Return pandas DataFrame with features from each nested file in data/raw/{dataset} directory."""

	recording_path = "data/raw/{x}".format(x=dataset)

	print(recording_path)

	all_files = [os.path.join(root, name)
	             for root, dirs, files in os.walk(recording_path)
	             for name in files]
	critical_files = [f for f in all_files if "_all" not in f and "DS" not in f and (".wav" in f or ".mp3" in f)]

	information = []
	for filepath in tqdm(critical_files):
		file_features = extract_file_features(filepath)		
		information.append(file_features)

	return pd.DataFrame(information)


if __name__ == "__main__":
	from argparse import ArgumentParser

	parser = ArgumentParser(description='Process audio files.')
	parser.add_argument('--dataset', dest="dataset", type=str, default="scaled_stimuli")

	args = vars(parser.parse_args())

	df = main(**args)
	df.to_csv("data/processed/exp1/audio_features_{x}.csv".format(x=args['dataset']))

