from src.entity.jungleWood import JungleWood

def test_initialization():
    junglewood = JungleWood()
    
    assert(junglewood.name == "Jungle Wood")
    assert(junglewood.getImagePath() == "assets/jungleWood.png")
    assert(junglewood.isSolid() == True)