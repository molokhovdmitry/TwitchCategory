# TwitchCategory
## About the project
Recognizes twitch stream category (not a game, game(specify game)) with a neural network.\
Input: channel name\
Output: category

### Part 1. Getting data:
- Figure out what category to update
  - Get top categories
  - Update database categories
  - Get database information (which category has less data)
  - Choose category
- Add data to database
  - Search channels that are live in this category\
  https://dev.twitch.tv/docs/v5/reference/search#search-streams
  - Get stream frames
  - Put images into the database (numpy arrays)
### Part 2. Training NN.
- Create simple NN for the start
- Test app
- Create more complex NN
### Part 3. Recognizing category.
- Get input (channel name)
- Get stream frames
- Load model
- Categorize frames
- Output top category
