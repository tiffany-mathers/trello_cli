
import requests
import argparse
import os
from dotenv import load_dotenv

# import Trello credentials and Board ID
load_dotenv()
API_KEY = os.environ.get("API_KEY")
TOKEN = os.environ.get("TOKEN")
BOARD_ID = os.environ.get("BOARD_ID")

BASE_URL = 'https://api.trello.com/1/'


def get_request(endpoint, params={}):
    """
    Request information from the Trello API
    """
    params['key'] = API_KEY
    params['token'] = TOKEN
    response = requests.get(BASE_URL + endpoint, params=params)
    # Add some error handling
    try:
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except requests.exceptions.RequestException as err:
        print(f'Error occurred: {err}')
    except ValueError:
        print(f'Error decoding JSON: {response.text}')
    return None

def list_lists(args=None):
    """
    Function that returns all the columns, or lists, from the Trello Board
    """
    lists = get_request(f"boards/{BOARD_ID}/lists")
    for _list in lists:
        print(f"List Name: {_list['name']}, ID: {_list['id']}")

def list_boards(args=None):
    """
    Function that returns all the boards in an account
    """
    boards = get_request('members/me/boards')
    for board in boards:
        print(f'Board Name: {board['name']}, ID: {board['id']}')

def list_cards(args=None):
    """
    Function that returns all the cards from the Trello Board
    """
    cards = get_request(f'boards/{BOARD_ID}/cards')
    for card in cards:
        # Display the card's name and ID. 
        print(f"Card Name: {card['name']}, ID: {card['id']}")

def list_labels(args=None):
    """
    Function that returns all the labels from the board
    """
    labels = get_request(f'boards/{BOARD_ID}/labels')
    for label in labels:
    # Display the labels' names and IDs
        print(f"Label Name: {label['name']}, ID: {label['id']}")
 
def create_card(args):
    """
    Function to create cards
    :param key: API Key 
    :param token: API Token
    :param idList: Trello list that the card will be added to
    :param name: Name of the Trello Card
    :param desc: Description of the Trello Card
    """
    params = {
    'key': API_KEY,
    'token': TOKEN,
    'idList': args.list_id,
    'name': args.title,
    'desc': args.desc,
    }

    # Check is the user wants to add any labels, before adding them to the parameters
    if args.labels:
        params['idLabels'] = str(args.labels)

    response = requests.post(f'{BASE_URL}cards', params=params)
    # Add some error handling
    try:
        response.raise_for_status()
        new_card = response.json()
        # Display success message with ID
        print(f"Card '{new_card['name']}' created with ID {new_card['id']}")
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except requests.exceptions.RequestException as err:
        print(f'Error occurred: {err}')
    except ValueError:
        print(f'Error decoding JSON: {response.text}')

def create_label(args):
    """
    Function to create labels
    :param key: API Key
    :param token: API Token
    :param idBoard: Trello Board ID
    :param name: Name of Label
    :param color: Color of Label
    """
    params = {
    'key': API_KEY,
    'token': TOKEN,
    'idBoard': BOARD_ID,
    'name': args.name,
    'color': args.color
    }
    response = requests.post(f'{BASE_URL}labels', params=params)
    # Add some error handling
    try:
        response.raise_for_status()
        new_label = response.json()
        # Display success message with ID
        print(f"Label '{new_label['name']}' created with ID {new_label['id']}")
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except requests.exceptions.RequestException as err:
        print(f'Error occurred: {err}')
    except ValueError:
        print(f'Error decoding JSON: {response.text}')


def create_comment(args):
    """
    Function to create comment
    :param card_id: Comment will be attached to this card
    :param text: Comment text
    """
    params = {
    'key': API_KEY,
    'token': TOKEN,
    'text': args.text
    }

    response = requests.post(f'{BASE_URL}cards/{args.card_id}/actions/comments', params=params)
    # Add some error handling
    try:
        response.raise_for_status()
        new_comment = response.json()
    # Display success message with ID
        print(f"Comment created with ID {new_comment['id']}")
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except requests.exceptions.RequestException as err:
        print(f'Error occurred: {err}')
    except ValueError:
        print(f'Error decoding JSON: {response.text}')

def main():
    parser = argparse.ArgumentParser(
        prog='Trello Board Management CLI',
        description='Trello Board Management CLI',
        epilog='Hope this helps'
        )

    subparsers = parser.add_subparsers(help='Sub-command help')

    # Add subparsers so we can add multiple subcommands, with their own arguments.
    # Each subparser will set a default function to be called.

    list_boards_parser = subparsers.add_parser('list-boards', aliases=['lb'], help='List all boards in an account')
    list_boards_parser.set_defaults(func=list_boards)

    list_lists_parser = subparsers.add_parser('list-lists', aliases=['ll'], help='List all lists on a board')
    list_lists_parser.set_defaults(func=list_lists)

    list_cards_parser = subparsers.add_parser('list-cards', aliases=['lc'], help='List all cards on a list')
    list_cards_parser.set_defaults(func=list_cards)

    list_labels_parser = subparsers.add_parser('list-labels', aliases=['llb'], help='List all labels on a board')
    list_labels_parser.set_defaults(func=list_labels)

    create_card_parser = subparsers.add_parser('create-card', aliases=['cc'], help='Create a new card on a list')
    create_card_parser.add_argument('-list_id', required=True, help='List ID')
    create_card_parser.add_argument('-title', required=True, help='Card Title')
    create_card_parser.add_argument('-desc', required=True, help='Card Description')
    # Labels are optional
    create_card_parser.add_argument('-labels', help='Card Labels (comma-separated)')
    create_card_parser.set_defaults(func=create_card)

    create_label_parser = subparsers.add_parser('create-label', aliases=['cl'], help='Create a new label on a board')
    create_label_parser.add_argument('-name', required=True, help='Label Name')
    create_label_parser.add_argument('-color', required=True, help='Label Color')
    create_label_parser.set_defaults(func=create_label)

    create_comment_parser = subparsers.add_parser('create-comment', aliases=['ccm'], help='Create a new comment on a card')
    create_comment_parser.add_argument('-card_id', required=True, help='Card ID')
    create_comment_parser.add_argument('-text', required=True, help='Comment Text')
    create_comment_parser.set_defaults(func=create_comment)

    args = parser.parse_args()


    # Check if the user has provided any arguments, if they haven't prompt them with a help message
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
