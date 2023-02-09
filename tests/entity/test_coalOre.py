from src.entity.coalOre import CoalOre

def test_initialization():
    coalore = CoalOre()
    
    assert(coalore.name == "Coal Ore")
    assert(coalore.getImagePath() == "assets/coalOre.png")
    assert(coalore.isSolid() == True)