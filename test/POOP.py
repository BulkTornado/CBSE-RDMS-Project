

class Car:
	def __init__(self, model: str, year: int, color: str, in_use: bool):
		self._model = model
		self._year = year
		self._color = color
		self.in_use = in_use
	
	def age(self, current_year: int) -> int:
		return current_year - self._year
	
	def __str__(self) -> str:
		return f"Model: {self._model}, Color: {self._color}, Manufactured in: {self._year}, and is currently {"in" if self.in_use else "not in"} use"
	
	def __repr__(self) -> str:
		return f"Car(model=\"{self._model}\", year={self._year}, color=\"{self._color}\", in_use={self.in_use})"
	
car1 = Car("Mustang", 1999, "yellow", True)

print(repr(car1))
