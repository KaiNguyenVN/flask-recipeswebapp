class Nutrition:
# TODO: Complete the implementation of the Nutrition class.
    def __init__(self, id: int, calories: int = None, fat: int = None,
                 saturatedfat: int = None, cholesterol:int = None,
                 sodium: int = None, carbohydrates: int = None,
                 fiber: int = None, sugar:int = None, protein:int = None) -> None:
        self.__id = id
        self.__calories = calories
        self.__fat = fat
        self.__saturatedfat = saturatedfat
        self.__cholesterol = cholesterol
        self.__sodium = sodium
        self.__carbohydrates = carbohydrates
        self.__fiber = fiber
        self.__sugar = sugar
        self.__protein = protein


        @property
        def id(self) -> int:
            return self.__id
        @property
        def calories(self) -> int:
            return self.__calories
        @property
        def fat(self) -> int:
            return self.__fat
        @property
        def saturatedfat(self) -> int:
            return self.__saturatedfat
        @property
        def cholesterol(self) -> int:
            return self.__cholesterol
        @property
        def sodium(self) -> int:
            return self.__sodium
        @property
        def carbohydrates(self) -> int:
            return self.__carbohydrates
        @property
        def fiber(self) -> int:
            return self.__fiber
        @property
        def sugar(self) -> int:
            return self.__sugar
        @property
        def protein(self) -> int:
            return self.__protein
