# Trello Board Management CLI

This script provides a command-line interface (CLI) for managing your Trello boards. You can list lists, cards, labels, create new cards, labels, and comments on your Trello board.

## Features
* List all lists on a Trello board
* List all cards on a Trello board  
* List all labels on a Trello board
* Create new cards with optional labels
* Create new labels
* Add comments to cards

## Installation

Set up a virtual environment:

```
  python3 -m venv .venv
  source .venv/bin/activate
```
Install the required packages:
```  
  pip install -r requirements.txt
```
Install the script:
``` 
  pip install .
```

## Configuration

The script uses your Trello API key, token and Trello board ID. Directions on how to locate this can be found here: https://developer.atlassian.com/cloud/trello/guides/rest-api/api-introduction/. You can find the board ID by logging into the Trellow account and exporting the board as JSON. More information can be found here: https://support.atlassian.com/trello/docs/exporting-data-from-trello/



You need to set these in a .env file in the root directory:
```
  API_KEY = 'your_api_key'
  TOKEN = 'your_token'
  BOARD_ID = 'your_board_id'
```


 You can also find the correct board ID by running `trello list-boards` as the first command of the script, then copying the correct board ID.


## Usage

Once installed, you can use the trello command from the terminal.

List all boards in an account
  ``` 
  trello list-boards
  ```
List all lists on a board
  ``` 
  trello list-lists
  ```
List all cards on a board
  ```
  trello list-cards
  ```
List all labels on a board
 ``` 
 trello list-labels
 ```
Create a new card
  ```
  trello create-card -list_id LIST_ID -title "Card Title" -desc "Card Description" -labels "Label1,Label2"
  ```
Create a new label
  ```
  trello create-label -name "Label Name" -color "Label Color"
  ```
Add a comment to a card
  ```
  trello create-comment -card_id CARD_ID -text "Comment Text"
  ```

## Next Development Steps
* Implement a more user-friendly interface for retrieving the board ID.