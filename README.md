# TwitchCategory
## About the project
### 1. Data Module.
Creates a dataset of twitch stream frames by downloading
frames from livestreams in popular categories.
![data](/images/data.png)
### 2. Model Module.
Trains a CNN model with the downloaded dataset.
![model](/images/model.png)
### 3. Recognition Module.
Recognizes livestream category by downloading frames,
predicting their categories with the model and calculating
the sum of the output tensors.
![recognition](/images/recognition.png)
