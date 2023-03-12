from unittest.mock import MagicMock
from src.world import tickCounter
from src.config import config

def createTickCounter():
    config.pygame = MagicMock()
    configInstance = config.Config()
    return tickCounter.TickCounter(configInstance)

def test_initialization():
    tc = createTickCounter()
    assert tc.getTick() == 0
    
def test_incrementTick():
    tc = createTickCounter()
    tc.incrementTick()
    assert tc.getTick() == 1
    assert True

# def test_updateMeasuredTicksPerSecond():
#     # TODO: implement test
#     assert(False)

# def test_getMeasuredTicksPerSecond():
#     # TODO: implement test
#     assert(False)

# def test_getHighestMeasuredTicksPerSecond():
#     # TODO: implement test
#     assert(False)
    
# def test_save():
#     # TODO: implement test
#     assert(False)

# def test_load():
#     # TODO: implement test
#     assert(False)