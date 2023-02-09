import pytest
from src.entity.living.livingEntity import LivingEntity

def test_initialization():
    livingEntity = LivingEntity("test", "myimagepath.png", 50, [], 0)
    
    assert(livingEntity.name == "test")
    assert(livingEntity.getEnergy() == 50)
    assert(livingEntity.getTargetEnergy() == 50)
    assert(livingEntity.getTickCreated() == 0)

def test_set_energy():
    livingEntity = LivingEntity("test", "myimagepath.png", 50, [], 0)
    livingEntity.setEnergy(100)
    
    assert(livingEntity.getEnergy() == 100)
    

def test_set_target_energy():
    livingEntity = LivingEntity("test", "myimagepath.png", 50, [], 0)
    livingEntity.setTargetEnergy(100)
    
    assert(livingEntity.getTargetEnergy() == 100)

def test_add_energy():
    livingEntity = LivingEntity("test", "myimagepath.png", 50, [], 0)
    livingEntity.addEnergy(50)
    
    assert(livingEntity.getEnergy() == 100)

def test_remove_energy():
    livingEntity = LivingEntity("test", "myimagepath.png", 50, [], 0)
    livingEntity.removeEnergy(50)
    
    assert(livingEntity.getEnergy() == 0)

def test_needs_energy():
    livingEntity = LivingEntity("test", "myimagepath.png", 50, [], 0)
    assert(livingEntity.needsEnergy() == False)
    
    livingEntity.setEnergy(livingEntity.getTargetEnergy() / 2 - 1)
    assert(livingEntity.needsEnergy() == True)

def test_get_age():
    livingEntity = LivingEntity("test", "myimagepath.png", 50, [], 0)
    assert(livingEntity.getAge(100) == 100)

def test_kill():
    livingEntity = LivingEntity("test", "myimagepath.png", 50, [], 0)
    livingEntity.kill()
    
    assert(livingEntity.getEnergy() == 0)

def test_can_eat():
    livingEntity = LivingEntity("test", "myimagepath.png", 50, [], 0)
    assert(livingEntity.canEat("test") == False)