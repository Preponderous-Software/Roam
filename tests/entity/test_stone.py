from src.entity.stone import Stone


def test_initialization():
    stone = Stone()

    assert stone.name == "Stone"
    assert stone.getImagePath() == "assets/images/stone.png"
    assert stone.isSolid() == True
