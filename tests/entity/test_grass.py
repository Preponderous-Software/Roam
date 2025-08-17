from src.entity.grass import Grass


def test_initialization():
    grass = Grass()

    assert grass.name == "Grass"
    assert grass.getImagePath() == "assets/images/grass.png"
    assert grass.isSolid() == False
