from src.entity.leaves import Leaves

def test_initialization():
    leaves = Leaves()
    
    assert(leaves.name == "Leaves")
    assert(leaves.getImagePath() == "assets/leaves.png")
    assert(leaves.isSolid() == False)