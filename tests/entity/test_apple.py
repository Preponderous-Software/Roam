from src.entity.apple import Apple


def test_initialization():
    apple = Apple()

    assert apple.name == "Apple"
    assert apple.getImagePath() == "assets/images/apple.png"
    assert apple.isSolid() == False
