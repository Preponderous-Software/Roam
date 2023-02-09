from src.entity.living.chicken import Chicken

def test_initialization():
    chicken = Chicken(0)
    
    assert(chicken.name == "Chicken")
    assert(chicken.getTickCreated() == 0)
    assert(chicken.getImagePath() == "assets/chicken.png")

def test_can_eat():
    chicken = Chicken(0)
    assert(chicken.canEat("test") == False)