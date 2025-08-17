from src.entity.food import Food


def test_initialization():
    food = Food("test", "myimagepath.png", 20)

    assert food.getName() == "test"
    assert food.getImagePath() == "myimagepath.png"
    assert food.getEnergy() == 20
