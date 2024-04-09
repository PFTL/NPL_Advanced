def check_birth_year(func):
    def wrapper(cls, *args):
        if cls.birth_year is None:
            print('Birth year not defined')
            return
        return func(cls, *args)
    return wrapper


class Person:
    def __init__(self, name):
        self.name = name
        self.birth_year = None

    @check_birth_year
    def calculate_age(self):
        return 2024-self.birth_year

    @check_birth_year
    def is_over_age(self, age_limit=18):
        return 2024-self.birth_year > age_limit


me = Person('Aquiles')
me.calculate_age()
me.is_over_age()
me.birth_year = 1986
print(me.is_over_age(41))