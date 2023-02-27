from src.entity.drawableEntity import DrawableEntity


def test_initialization():
    drawableEntity = DrawableEntity("test", "myimagepath.png")

    assert drawableEntity.getName() == "test"
    assert drawableEntity.getImagePath() == "myimagepath.png"
