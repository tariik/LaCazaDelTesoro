from distutils.command.install_data import install_data
from google.appengine.ext import db
from models.entities.game import Game


def get_or_insert_game(zone=None, treasures=None, owner=None, name=None, is_active=True):
    """Get or insert the game with the information provided

        Args:
            :param is_active: Allows knowing if the game is active or not.
                :type: Boolean
            :param name: The name that receives the game.
                :type: String
            :param owner: The user who is the owner of the game
                :type: User
            :param treasures: The list of treasures the participants need to find to win the game
                :type: [Treasure]
            :param zone: The zone where the treasures are located
                :type: Zone
        Raises:
            Exception: if the required parameters are not present or are None
        Returns:
            Game: The game from db or the one which was just created
    """
    if name is None or owner is None or owner.email is None:
        return None
    game = Game.get_or_insert(key_name=owner.email + "_" + name, is_active=is_active, name=name, zone=zone,
                              treasures=treasures, owner=owner, participants=[], winner=None)
    return game


def delete_game(game=None):
    """Delete the game from db

        Args:
            :param game: The game which is going to be deleted from db
                :type: Game
    """
    db.delete(game)


def get_game_by_owner_and_name(owner=None, game_name=None):
    """Get the game from db whose name is "game_name" and the owner is "owner"
        Args:
            :param owner: The owner of the game to obtain
                :type: User
            :param game_name: The name of the game to obtain
                :type: String
    """
    if owner is None or owner.email is None or game_name is None:
        return None
    return Game.get_by_key_name(key_names=owner.email + "_" + game_name)


def get_game_by_id(_id=None):
    """Get the game from db with the id provided
        Args:
            :param _id: The id of the game to search in db
                :type: Game
        Returns:
            Game: The game if it is already stored, None in other case
    """
    if _id is None:
        return None
    return Game.get_by_id(ids=_id)


def exists_game(game=None):
    """Get a boolean value corresponding with the evidence of an existing game provided in db
        Args:
            :param game: The game to search in db
                :type: Game
        Returns:
            Boolean: Specify if the game is already stored in db
    """
    if game is None or game.name is None or game.owner is None or game.owner.email is None:
        return False
    return Game.get_by_key_name(key_names=game.owner.email + "_" + game.name) is not None
