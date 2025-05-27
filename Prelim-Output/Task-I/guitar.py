# Tagle, Marc Neil V. - M001

import random as rd

class Guitar:
    def __init__(self, color, brand, type="acoustic", strings=6) -> None:
        self._color = color
        self._brand = brand
        self._type = type
        self._strings = strings
        self._is_tuned = False
    
    @property
    def color(self) -> str:
        return self._color
    
    @color.setter
    def color(self, color) -> None:
        self._color = color

    @property
    def brand(self) -> str:
        return self._brand
    
    @brand.setter
    def brand(self, brand) -> None:
        self._brand = brand

    @property
    def type(self) -> str:
        return self._type

    @type.setter
    def type(self, type) -> None:
        self._strings = type

    @property
    def strings(self) -> int:
        return self._strings

    @strings.setter
    def strings(self, strings) -> None:
        self._strings = strings

    def play_a_chord(self) -> str:
        if self._is_tuned:
            chords = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
            tonalities = ['major', 'minor']
            random_chord = rd.choice(chords)
            random_tonality = rd.choice(tonalities)
            article = "an" if random_chord in 'AEF' else "a"
            return f"Playing {article} {random_chord} {random_tonality} chord!"
        else:
            return f"Tune your {self._type} guitar first!"
    
    def change_strings(self) -> str:
        return f"Your {self._type} guitar's strings are changed!"
    
    def tune(self) -> str:
        self._is_tuned = True
        return f"Your {self._type} guitar is now tuned!"

    def play_a_song(self, song_name, song_artist="Unknown") -> str:
        if self._is_tuned:
            return f"Playing {song_name} by {song_artist}!"
        else:
            return f"Tune your {self._type} guitar first!"
        
    def practice(self, duration) -> str:
        if not self._is_tuned:
            return f"Tune your {self._type} guitar first!"
        if duration < 1:
            return f"You're not practicing!"
        if duration >= 60:
            hours_value = duration // 60
            hours = 'hours' if hours_value > 1 else 'hour'
            minutes_value = duration % 60
            minutes = 'minutes' if minutes_value > 1 else 'minute'
            if minutes_value == 0:
                return f"Practicing for {hours_value} {hours}!"
            return f"Practicing for {hours_value} {hours} and {minutes_value} {minutes}!" 
        return f"Practicing for {duration} {'minutes' if duration > 1 else 'minute'}!"
    
    def __str__(self) -> str:
        return (f"Guitar Details:\n"
                f"Type: {self._type}\n"
                f"Brand: {self._brand}\n"
                f"Color: {self._color}\n"
                f"Strings: {self._strings}\n"
                f"Tuned: {'Yes' if self._is_tuned else 'No'}")