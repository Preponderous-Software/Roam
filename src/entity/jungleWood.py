from entity.drawableEntity import DrawableEntity


# @author Daniel McCoy Stephenson
# @since August 8th, 2022
class JungleWood(DrawableEntity):
    def __init__(self):
        DrawableEntity.__init__(self, "Jungle Wood", "assets/images/jungleWood.png")
        self.solid = True

    def isSolid(self):
        return self.solid
