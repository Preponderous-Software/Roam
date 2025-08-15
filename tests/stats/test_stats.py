from unittest.mock import MagicMock
from src.stats.stats import Stats


def createStatsInstance():
    config = MagicMock()
    config.pathToSaveDirectory = "tests/stats"
    return Stats(config)


def test_initialization():
    # call
    stats = createStatsInstance()

    # check
    assert stats.getScore() == 0
    assert stats.getRoomsExplored() == 0
    assert stats.getFoodEaten() == 0
    assert stats.getNumberOfDeaths() == 0


def test_setScore():
    # prepare
    stats = createStatsInstance()

    # call
    stats.setScore(5)

    # check
    assert stats.getScore() == 5


def test_setRoomsExplored():
    # prepare
    stats = createStatsInstance()

    # call
    stats.setRoomsExplored(5)

    # check
    assert stats.getRoomsExplored() == 5


def test_setFoodEaten():
    # prepare
    stats = createStatsInstance()

    # call
    stats.setFoodEaten(5)

    # check
    assert stats.getFoodEaten() == 5


def test_setNumberOfDeaths():
    # prepare
    stats = createStatsInstance()

    # call
    stats.setNumberOfDeaths(5)

    # check
    assert stats.getNumberOfDeaths() == 5


def test_incrementScore():
    # prepare
    stats = createStatsInstance()

    # call
    stats.incrementScore()

    # check
    assert stats.getScore() == 1


def test_incrementRoomsExplored():
    # prepare
    stats = createStatsInstance()

    # call
    stats.incrementRoomsExplored()

    # check
    assert stats.getRoomsExplored() == 1


def test_incrementFoodEaten():
    # prepare
    stats = createStatsInstance()

    # call
    stats.incrementFoodEaten()

    # check
    assert stats.getFoodEaten() == 1


def test_incrementNumberOfDeaths():
    # prepare
    stats = createStatsInstance()

    # call
    stats.incrementNumberOfDeaths()

    # check
    assert stats.getNumberOfDeaths() == 1


def test_save():
    # prepare
    stats = createStatsInstance()
    stats.incrementScore()
    stats.incrementRoomsExplored()
    stats.incrementFoodEaten()
    stats.incrementNumberOfDeaths()

    # call
    stats.save()

    # check
    assert stats.getScore() == 1
    assert stats.getRoomsExplored() == 1
    assert stats.getFoodEaten() == 1
    assert stats.getNumberOfDeaths() == 1


def test_load():
    # prepare
    stats = createStatsInstance()
    stats.incrementScore()
    stats.incrementRoomsExplored()
    stats.incrementFoodEaten()
    stats.incrementNumberOfDeaths()

    # call
    stats.load()

    # check
    assert stats.getScore() == 1
    assert stats.getRoomsExplored() == 1
    assert stats.getFoodEaten() == 1
    assert stats.getNumberOfDeaths() == 1
