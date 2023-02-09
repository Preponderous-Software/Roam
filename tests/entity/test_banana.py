from src.entity.banana import Banana

def test_initialization():
    banana = Banana()
    
    assert(banana.name == "Banana")
    assert(banana.getImagePath() == "assets/banana.png")
    assert(banana.isSolid() == False)