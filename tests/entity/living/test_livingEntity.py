from src.entity.living.livingEntity import LivingEntity


def createLivingEntity():
    return LivingEntity("test", "myimagepath.png", 50, [], 0)


def test_initialization():
    livingEntity = createLivingEntity()

    assert livingEntity.name == "test"
    assert livingEntity.getEnergy() == 50
    assert livingEntity.getTargetEnergy() == 50
    assert livingEntity.getTickCreated() == 0


def test_set_energy():
    livingEntity = createLivingEntity()
    livingEntity.setEnergy(100)

    assert livingEntity.getEnergy() == 100


def test_set_target_energy():
    livingEntity = createLivingEntity()
    livingEntity.setTargetEnergy(100)

    assert livingEntity.getTargetEnergy() == 100


def test_add_energy():
    livingEntity = createLivingEntity()
    livingEntity.addEnergy(50)

    assert livingEntity.getEnergy() == 100


def test_remove_energy():
    livingEntity = createLivingEntity()
    livingEntity.removeEnergy(50)

    assert livingEntity.getEnergy() == 0


def test_needs_energy():
    livingEntity = createLivingEntity()
    assert livingEntity.needsEnergy() == False

    livingEntity.setEnergy(livingEntity.getTargetEnergy() / 2 - 1)
    assert livingEntity.needsEnergy() == True


def test_get_age():
    livingEntity = createLivingEntity()
    assert livingEntity.getAge(100) == 100


def test_kill():
    livingEntity = createLivingEntity()
    livingEntity.kill()

    assert livingEntity.getEnergy() == 0


def test_can_eat():
    livingEntity = createLivingEntity()
    assert livingEntity.canEat("test") == False
