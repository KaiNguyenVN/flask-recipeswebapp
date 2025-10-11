from recipe.domainmodel.recipe import Recipe


class Nutrition:
# TODO: Complete the implementation of the Nutrition class.
#nutrition id is basically recipes id
    def __init__(self, id: int, calories: float = None, fat: float = None,
                 saturated_fat: float = None, cholesterol:float = None,
                 sodium: float = None, carbohydrates: float = None,
                 fiber: float = None, sugar:float = None, protein:float = None) -> None:
        self.__id = id
        self.__calories = calories
        self.__fat = fat
        self.__saturated_fat = saturated_fat
        self.__cholesterol = cholesterol
        self.__sodium = sodium
        self.__carbohydrates = carbohydrates
        self.__fiber = fiber
        self.__sugar = sugar
        self.__protein = protein

    def __repr__(self):
        return f"calories:{self.__calories}, fat:{self.__fat}, saturated_fat:{self.__saturated_fat}, cholesterol:{self.__cholesterol}, sodium:{self.__sodium}, protein:{self.__protein}, fiber:{self.__fiber}, sugar:{self.__sugar}, carbohydrates:{self.__carbohydrates}"

    def __eq__(self, other):
        if isinstance(other, Nutrition):
            return self.__id == other.__id
        else:
            raise TypeError("Comparison must be between Nutrition instances")

    def __lt__(self, other):
        if isinstance(other, Nutrition):
            return self.id < other.id
        else:
            raise TypeError("Comparison must be between Nutrition instances")

    def __hash__(self) -> int:
       return hash(self.id)




    @property
    def id(self) -> int:
        return self.__id


    @property
    def calories(self) -> float:
        return self.__calories


    @property
    def fat(self) -> float:
        return self.__fat


    @property
    def saturated_fat(self) -> float:
        return self.__saturated_fat


    @property
    def cholesterol(self) -> float:
        return self.__cholesterol


    @property
    def sodium(self) -> float:
        return self.__sodium


    @property
    def carbohydrates(self) -> float:
        return self.__carbohydrates


    @property
    def fiber(self) -> float:
        return self.__fiber


    @property
    def sugar(self) -> float:
        return self.__sugar


    @property
    def protein(self) -> float:
        return self.__protein

    def calculate_health_stars(self) -> float|None:

        # Baseline points (negative)
        baseline = 0
        # thresholds are per 100g/ml (simplified)
        if self.saturated_fat:
            if self.saturated_fat <= 1:
                baseline += 0
            elif self.saturated_fat <= 3:
                baseline += 1
            elif self.saturated_fat <= 5:
                baseline += 2
            else:
                baseline += 3

        if self.sugar:
            if self.sugar <= 5:
                baseline += 0
            elif self.sugar <= 10:
                baseline += 1
            elif self.sugar <= 15:
                baseline += 2
            else:
                baseline += 3

        if self.sodium:
            if self.sodium <= 120:
                baseline += 0
            elif self.sodium <= 200:
                baseline += 1
            elif self.sodium <= 400:
                baseline += 2
            else:
                baseline += 3

        # Modifying points (positive)
        modifying = 0
        if self.fiber:
            if self.fiber >= 4: modifying += 1
            if self.fiber >= 8: modifying += 1  # extra point for very high fiber
        if self.protein:
            if self.protein >= 5: modifying += 1
            if self.protein >= 10: modifying += 1

        # Calculate final star score
        score = 5 - baseline + modifying
        # clamp to 0.5 - 5 stars
        return max(0.5, min(5, round(score * 2) / 2))