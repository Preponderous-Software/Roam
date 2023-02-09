from src.entity.oakWood import OakWood

def test_initialization():
    oakwood = OakWood()
    
    assert(oakwood.name == "Oak Wood")
    assert(oakwood.getImagePath() == "assets/oakWood.png")
    assert(oakwood.isSolid() == True)