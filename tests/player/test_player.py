from unittest.mock import MagicMock
from src.player import player


def createPlayerInstance():
    player.Inventory = MagicMock()
    return player.Player(0)


def test_initialization():
    # call
    playerInstance = createPlayerInstance()

    # check
    assert playerInstance.getDirection() == -1
    assert playerInstance.getLastDirection() == -1
    assert playerInstance.isGathering() == False
    assert playerInstance.isPlacing() == False
    assert playerInstance.isDead() == False
    assert playerInstance.getTickLastMoved() == -1
    assert playerInstance.getMovementSpeed() == 30
    assert playerInstance.getGatherSpeed() == 30
    assert playerInstance.getPlaceSpeed() == 30
    assert playerInstance.isCrouching() == False
    assert playerInstance.isSolid() == False

    player.Inventory.assert_called_once()


def test_set_direction_up():
    # prepare
    playerInstance = createPlayerInstance()

    # call
    playerInstance.setDirection(0)

    # check
    assert playerInstance.getDirection() == 0
    assert playerInstance.getLastDirection() == -1
    assert playerInstance.imagePath == "assets/images/player_up.png"


def test_set_direction_left():
    # prepare
    playerInstance = createPlayerInstance()

    # call
    playerInstance.setDirection(1)

    # check
    assert playerInstance.getDirection() == 1
    assert playerInstance.getLastDirection() == -1
    assert playerInstance.imagePath == "assets/images/player_left.png"


def test_set_direction_down():
    # prepare
    playerInstance = createPlayerInstance()

    # call
    playerInstance.setDirection(2)

    # check
    assert playerInstance.getDirection() == 2
    assert playerInstance.getLastDirection() == -1
    assert playerInstance.imagePath == "assets/images/player_down.png"


def test_set_direction_right():
    # prepare
    playerInstance = createPlayerInstance()

    # call
    playerInstance.setDirection(3)

    # check
    assert playerInstance.getDirection() == 3
    assert playerInstance.getLastDirection() == -1
    assert playerInstance.imagePath == "assets/images/player_right.png"


def test_set_gathering():
    # prepare
    playerInstance = createPlayerInstance()

    # call
    playerInstance.setGathering(True)

    # check
    assert playerInstance.isGathering() == True


def test_set_placing():
    # prepare
    playerInstance = createPlayerInstance()

    # call
    playerInstance.setPlacing(True)

    # check
    assert playerInstance.isPlacing() == True


def test_set_tick_last_moved():
    # prepare
    playerInstance = createPlayerInstance()

    # call
    playerInstance.setTickLastMoved(10)

    # check
    assert playerInstance.getTickLastMoved() == 10


def test_set_inventory():
    # prepare
    playerInstance = createPlayerInstance()
    inventory = MagicMock()

    # call
    playerInstance.setInventory(inventory)

    # check
    assert playerInstance.getInventory() == inventory


def test_set_movement_speed():
    # prepare
    playerInstance = createPlayerInstance()

    # call
    playerInstance.setMovementSpeed(10)

    # check
    assert playerInstance.movementSpeed == 10


def test_set_gather_speed():
    # prepare
    playerInstance = createPlayerInstance()

    # call
    playerInstance.setGatherSpeed(10)

    # check
    assert playerInstance.gatherSpeed == 10


def test_set_place_speed():
    # prepare
    playerInstance = createPlayerInstance()

    # call
    playerInstance.setPlaceSpeed(10)

    # check
    assert playerInstance.placeSpeed == 10


def test_set_crouching():
    # prepare
    playerInstance = createPlayerInstance()

    # call
    playerInstance.setCrouching(True)

    # check
    assert playerInstance.crouching == True


def test_is_moving():
    # prepare
    playerInstance = createPlayerInstance()

    # call
    playerInstance.setDirection(0)

    # check
    assert playerInstance.isMoving() == True


def is_moving_false():
    # prepare
    playerInstance = createPlayerInstance()

    # call
    playerInstance.setDirection(-1)

    # check
    assert playerInstance.isMoving() == False
