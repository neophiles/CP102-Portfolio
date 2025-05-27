# Tagle, Marc Neil V. - M001

from guitar import Guitar

class BassGuitar(Guitar):
    def __init__(self, color, brand, model, pickups, strings=4) -> None:
        super().__init__(color, brand, "bass", strings)
        self._model = model
        self._pickups = pickups

    @property
    def model(self) -> str:
        return self._model

    @model.setter
    def model(self, model) -> None:
        self._model = model

    @property
    def pickups(self) -> str:
        return self._pickups

    @pickups.setter
    def pickups(self, pickups) -> None:
        self._pickups = pickups
    
    def slap_and_pop(self) -> str:
        if self._is_tuned:
            return "Slapping and popping that piece of furniture!"
        else:
            return f"Tune your {self._type} guitar first!"

    def fingerstyle(self) -> str:
        if self._is_tuned:
            return "Plucking the strings for melodic bassline."
        else:
            return f"Tune your {self._type} guitar first!"

    def slide(self) -> str:
        if self._is_tuned:
            return "Sliding along the neck for smooth transition between notes."
        else:
            return f"Tune your {self._type} guitar first!"

    def walk_a_bassline(self) -> str:
        if self._is_tuned:
            return "Walking a bassline for that smooth, jazzy feel."
        else:
            return f"Tune your {self._type} guitar first!"
        
    def __str__(self) -> str:
        parent_str = super().__str__()
        return f"{parent_str}\nModel: {self._model}\nPickups: {self._pickups}"