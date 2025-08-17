from src.entity.ironOre import IronOre


def test_initialization():
    ironore = IronOre()

    assert ironore.name == "Iron Ore"
    assert ironore.getImagePath() == "assets/images/ironOre.png"
    assert ironore.isSolid() == True
