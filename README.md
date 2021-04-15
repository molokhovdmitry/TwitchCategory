# TwitchCategory

## About the project

### 1. Data Module.
Creates a dataset of twitch stream frames by downloading
frames from livestreams in popular categories.
![data](/images/data.png)
Uses **Streamlink** to download frames, **OpenCV** to resize images,
**sqlalchemy** to store info in a **postgres** database.
![schema](/images/schema.svg)

### 2. Model Module.
Trains a CNN model with the downloaded dataset using tensorflow.
![model](/images/model.png)
Comes with a model trained on 2.5 GB of 240x240 images (2700 per
category).

<details>
<summary>Games</summary>

* ARK: Survival Evolved
* Among Us
* Apex Legends
* Bloons TD 6
* Call of Duty: Warzone
* Counter-Strike: Global Offensive
* Dead by Daylight
* Destiny 2
* Dota 2
* Enlisted
* Escape from Tarkov
* Euro Truck Simulator 2
* FIFA 21
* Fortnite
* Gartic Phone
* Grand Theft Auto V
* Hearthstone
* It Takes Two
* LOST ARK
* League of Legends
* League of Legends: Wild Rift
* Mario Kart 8 Deluxe
* Minecraft
* Outriders
* Overwatch
* PLAYERUNKNOWN'S BATTLEGROUNDS
* Rocket League
* Rust
* Sea of Thieves
* Teamfight Tactics
* The Binding of Isaac: Repentance
* Tom Clancy's Rainbow Six Siege
* Totally Accurate Battlegrounds
* VALORANT
* Valheim
* World of Warcraft

</details>

### 3. Recognition Module.
Recognizes livestream category by downloading frames,
predicting their categories with the model and calculating
the sum of the output tensors.
![recognition](/images/recognition.png)

## Requirements
* Python 3.6–3.8
* cuDNN 8.0
* CUDA 11.0

## Install

### Clone the repository and install the requirements:
```
git clone https://github.com/molokhovdmitry/TwitchCategory
cd TwitchCategory
pip install -r requirements.txt
```
### Setup the application by filling *config.py*
Default model training settings work with:
* 16 GB of RAM
* GTX 1660Ti

## How to use
### Data
Create and download the dataset with:
```
python -m data.download
```
To stop the downloading process press *Enter* in the terminal.

To show the dataset info and list the downloaded categories use:
```
python -m data.info
```

You can synchronize the database with the dataset after deleting games/frames from
the dataset with:
```
python -m data.dbSync
```

### Model
Train a model with the downloaded data with:
```
python -m model.create
```
This will create **model.h5** and **classes.txt** files.

### Recognition
Recognize stream category with:
```
python -m recognition.recognize login
```

### Example 1
![stream_1](/images/stream_1.jpg)
Input:
```
python -m recognition.recognize jasper7se
```
Output:
```
Frame 1: VALORANT with a 99.59% confidence.
Frame 2: VALORANT with a 100.00% confidence.
Frame 3: VALORANT with a 100.00% confidence.
Frame 4: VALORANT with a 100.00% confidence.
Frame 5: VALORANT with a 100.00% confidence.
Frame 6: VALORANT with a 100.00% confidence.
Frame 7: VALORANT with a 100.00% confidence.
Frame 8: VALORANT with a 100.00% confidence.
Frame 9: VALORANT with a 100.00% confidence.
Frame 10: VALORANT with a 100.00% confidence.
Frame 11: VALORANT with a 100.00% confidence.
Frame 12: VALORANT with a 100.00% confidence.
Frame 13: VALORANT with a 100.00% confidence.
VALORANT with a score of 5.6
```

### Example 2
![stream_2](/images/stream_2.jpg)
Input:
```
python -m recognition.recognize velloso
```
Output:
```
Frame 1: VALORANT with a 99.64% confidence.
Frame 2: VALORANT with a 98.60% confidence.
Frame 3: Overwatch with a 23.20% confidence.
Frame 4: VALORANT with a 66.41% confidence.
Frame 5: VALORANT with a 54.73% confidence.
Frame 6: VALORANT with a 74.28% confidence.
Frame 7: VALORANT with a 79.36% confidence.
Frame 8: VALORANT with a 80.69% confidence.
Frame 9: VALORANT with a 60.30% confidence.
Frame 10: VALORANT with a 78.39% confidence.
Frame 11: VALORANT with a 92.49% confidence.
Frame 12: VALORANT with a 87.56% confidence.
Frame 13: VALORANT with a 87.85% confidence.
VALORANT with a score of -5.0
```

### Example 3
![stream_3](/images/stream_3.jpg)
Input:
```
python -m recognition.recognize otplol_
```
Output:
```
Frame 1: League of Legends with a 100.00% confidence.
Frame 2: League of Legends with a 99.77% confidence.
Frame 3: League of Legends with a 99.41% confidence.
Frame 4: League of Legends with a 100.00% confidence.
Frame 5: League of Legends with a 99.38% confidence.
League of Legends with a score of -5.6
```

### Example 4
![stream_4](/images/stream_4.jpg)
Input:
```
python -m recognition.recognize buddha
```
Output:
```
Frame 1: Grand Theft Auto V with a 100.00% confidence.
Frame 2: Grand Theft Auto V with a 100.00% confidence.
Frame 3: Grand Theft Auto V with a 100.00% confidence.
Frame 4: Grand Theft Auto V with a 100.00% confidence.
Frame 5: Grand Theft Auto V with a 100.00% confidence.
Frame 6: Grand Theft Auto V with a 100.00% confidence.
Frame 7: Grand Theft Auto V with a 100.00% confidence.
Frame 8: Grand Theft Auto V with a 100.00% confidence.
Frame 9: Grand Theft Auto V with a 100.00% confidence.
Frame 10: Grand Theft Auto V with a 100.00% confidence.
Frame 11: Grand Theft Auto V with a 100.00% confidence.
Frame 12: Grand Theft Auto V with a 100.00% confidence.
Frame 13: Grand Theft Auto V with a 100.00% confidence.
Grand Theft Auto V with a score of 4.0
```
