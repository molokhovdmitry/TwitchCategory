# TwitchCategory

## About the project

### 1. Data Module.
Creates a dataset of twitch stream frames by downloading
frames from livestreams in popular categories.
![data](/images/data.png)
Uses Streamlink to download frames, OpenCV to resize images,
sqlalchemy to store info in a postgres database.

### 2. Model Module.
Trains a CNN model with the downloaded dataset using tensorflow.
![model](/images/model.png)
Comes with a model trained on 2 GB of 240x240 images.

<details>
<summary>Categories</summary>

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

## Installation

## How to use

## Example
