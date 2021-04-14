# Prosody

Scaled up version of behavioral prosody study, along with code to extract acoustic features of recorded stimuli, conduct R analyses, and produce figures. This corresponds to the submitted manuscript:

> Trott, S., Reed, S., Kaliblotzky, D., Ferreira, V., Bergen, B. (Submitted) The role of prosody in disambiguating English indirect requests.

# Data

The **raw recordings** can be found in `data/raw/scaled_stimuli`. Each utterance recording is listed in a separate file, following the convention:

```{speaker_ID}_{intent}_{item}.wav```

The **acoustic features** can be found in `data/processed/audio/audio_features_scaled_stimuli.csv`.

The **norming data** can be found in `data/processed/norming/item_means.csv` and `data/processed/norming/norming_data.csv`.

Finally, the preprocessed data from the `behavioral experiment` can be found in `data/processed/behavioral/pros_scaled_processed.csv`.

# Analysis code

All analysis code can be found in the `src` folder:

- `src/analysis/audio`: `.Rmd` file for running the pre-registered acoustic features analysis.  
- `src/analysis/behavioral`: contains an `.Rmd` file for running the pre-registered analysis of the behavioral data.  
- `src/analysis/norming`: contains an `.Rmd` file for running the analysis of the norming experiment.


# Experiment

Finally, the code for the experiment itself can be found in `experiment/prosody_exp_full.html`. 
