# Tagle, Marc Neil V. - M001

from guitar import Guitar

class ElectricGuitar(Guitar):
    def __init__(self, color, brand, model, pickups, strings=6, has_whammy_bar=False) -> None:
        super().__init__(color, brand, "electric", strings)
        self._model = model
        self._pickups = pickups
        self._has_whammy_bar = has_whammy_bar

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

    @property
    def has_whammy_bar(self) -> bool:
        return self._has_whammy_bar
    
    @has_whammy_bar.setter
    def has_whammy_bar(self, has_whammy_bar):
        self._has_whammy_bar = has_whammy_bar
    
    def shred(self):
        if self._is_tuned:
            return "Shredding on an electric guitar!"
        else:
            return f"Tune your {self._type} guitar first!"
    
    def play_a_lick(self):
        if self._is_tuned:
            return "Playing a lick!"
        else:
            return f"Tune your {self._type} guitar first!"
    
    def solo(self):
        if self._is_tuned:
            return "Soloing on an electric guitar! Awesome!"
        else:
            return f"Tune your {self._type} guitar first!"
        
    def __str__(self) -> str:
        parent_str = super().__str__()
        return f"{parent_str}\nModel: {self._model}\nPickups: {self._pickups}"