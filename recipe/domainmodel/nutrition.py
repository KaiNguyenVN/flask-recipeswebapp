class Nutrition:
# TODO: Complete the implementation of the Nutrition class.
    def __init__(self, id: int, calories: float = None, fat: float = None,
                 saturatedfat: float = None, cholesterol:float = None,
                 sodium: float = None, carbohydrates: float = None,
                 fiber: float = None, sugar:float = None, protein:float = None) -> None:
        self.__id = id
        #self.__calories = calories
        #self.__fat = fat
        #self.__saturatedfat = saturatedfat
        #self.__cholesterol = cholesterol
        #self.__sodium = sodium
        #self.__carbohydrates = carbohydrates
        #self.__fiber = fiber
        #self.__sugar = sugar
        #self.__protein = protein
        self.__nutris = {"calories": calories, "fat": fat, "saturatedfat": saturatedfat, "cholesterol": cholesterol, "sodium": sodium, "carbohydrates": carbohydrates, "fiber": fiber , "sugar": sugar, "protein": protein}

        def __repr__(self):
            return str(self.__nutris)

        def __eq__(self, other, nutri):
            if isinstance(other, Nutrition):
                return self.__nutris[nutri] == other.__nutris[nutri]
            else:
                return False

        def __lt__(self, other, nutri):
            if isinstance(other, Nutrition):
                return self.__nutris[nutri] < other.__nutris[nutri]
            else:
                return False

        def __hash__(self) -> int:
            return hash(self.id)



        @property
        def id(self) -> int:
            return self.__id
        @property
        def calories(self) -> int:
            return self.__nutirs["calories"]
        @property
        def fat(self) -> int:
            return self.__nutris["fat"]
        @property
        def saturatedfat(self) -> int:
            return self.__nutris["saturatedfat"]
        @property
        def cholesterol(self) -> int:
            return self.__nutris["cholesterol"]
        @property
        def sodium(self) -> int:
            return self.__nutris["sodium"]
        @property
        def carbohydrates(self) -> int:
            return self.__nutris["carbohydrates"]
        @property
        def fiber(self) -> int:
            return self.__nutris["fiber"]
        @property
        def sugar(self) -> int:
            return self.__nutris["sugar"]
        @property
        def protein(self) -> int:
            return self.__nutris["protein"]