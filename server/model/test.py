from dataclasses import dataclass
from datetime import datetime

@dataclass
class Person:
    born: datetime

human = Person(born="asdfasd")
print(human.born)