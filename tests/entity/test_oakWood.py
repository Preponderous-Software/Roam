from src.entity.oakWood import OakWood


def test_initialization():
    oakwood = OakWood()

    assert oakwood.name == "Oak Wood"
    assert oakwood.getImagePath() == "assets/images/oakWood.png"
    assert oakwood.isSolid() == True
