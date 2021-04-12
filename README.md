# TwitchCategory

## About the project

### 1. Data Module.
Creates a dataset of twitch stream frames by downloading
frames from livestreams in popular categories.
![data](/images/data.png)
Uses Streamlink to download frames, OpenCV to resize images,
sqlalchemy to store info in a postgres database.
![schema](/images/schema.svg)

### 2. Model Module.
Trains a CNN model with the downloaded dataset using tensorflow.
![model](/images/model.png)
Comes with a model trained on 2 GB of 240x240 images.

<details>
<summary>Games</summary>

* ARK: Survival Evolved
* Among Us
* Apex Legends
* Brawlhalla
* Call Of Duty: Modern Warfare
* Call of Duty: Black Ops Cold War
* Call of Duty: Warzone
* Conqueror's Blade
* Counter-Strike: Global Offensive
* DOOM Eternal
* Dead by Daylight
* Destiny 2
* Dota 2
* Escape From Tarkov
* FIFA 21
* Fall Guys: Ultimate Knockout
* Fortnite
* Garena Free Fire
* Gartic Phone
* Grand Theft Auto V
* Hearthstone
* Hunt: Showdown
* LOST ARK
* League of Legends
* Magic: Legends
* Magic: The Gathering
* Mario Kart 8
* Minecraft
* Monster Hunter Rise
* Overwatch
* PLAYERUNKNOWN'S BATTLEGROUNDS
* Raft
* Risk of Rain 2
* Rocket League
* Satisfactory
* Teamfight Tactics
* The Elder Scrolls V: Skyrim
* Tom Clancy's Rainbow Six Siege
* VALORANT
* Warframe
* World of Warcraft
</details>

### 3. Recognition Module.
Recognizes livestream category by downloading frames,
predicting their categories with the model and calculating
the sum of the output tensors.
![recognition](/images/recognition.png)

## Install

### Clone the repository and install the requirements:
```
git clone https://github.com/molokhovdmitry/TwitchCategory
cd TwitchCategory
pip install -r requirements.txt
```
### Setup the application by filling *config.py*

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

You can clean the dataset and synchronize it with the database with:
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
