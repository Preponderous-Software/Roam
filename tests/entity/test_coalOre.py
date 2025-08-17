from src.entity.coalOre import CoalOre


def test_initialization():
    coalore = CoalOre()

    assert coalore.name == "Coal Ore"
    assert coalore.getImagePath() == "assets/images/coalOre.png"
    assert coalore.isSolid() == True
