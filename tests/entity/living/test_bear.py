from src.entity.living.bear import Bear


def test_initialization():
    bear = Bear(0)

    assert bear.name == "Bear"
    assert bear.getTickCreated() == 0
    assert bear.getImagePath() == "assets/images/bear.png"
    assert bear.isSolid() == False
