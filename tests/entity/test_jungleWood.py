from src.entity.jungleWood import JungleWood


def test_initialization():
    junglewood = JungleWood()

    assert junglewood.name == "Jungle Wood"
    assert junglewood.getImagePath() == "assets/images/jungleWood.png"
    assert junglewood.isSolid() == True
