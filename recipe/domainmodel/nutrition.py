class Nutrition:
# TODO: Complete the implementation of the Nutrition class.
#nutrition id is basically recipes id
    def __init__(self, recipe_id: int, calories: float = None, fat: float = None,
                 saturated_fat: float = None, cholesterol:float = None,
                 sodium: float = None, carbohydrates: float = None,
                 fiber: float = None, sugar:float = None, protein:float = None) -> None:
        self.__recipe_id = recipe_id
        self.__nutri_content = {"calories": calories, "fat": fat, "saturated_fat": saturated_fat, "cholesterol": cholesterol, "sodium": sodium, "carbohydrates": carbohydrates, "fiber": fiber , "sugar": sugar, "protein": protein}

    def __repr__(self):
        return str(self.__nutri_content)

    def __eq__(self, other, nutri_type):
        if isinstance(other, Nutrition):
            return self.__nutri_content[nutri_type] == other.__nutri_content[nutri_type]
        else:
            return False

    def __lt__(self, other, nutri):
        if isinstance(other, Nutrition):
            return self.__nutri_content[nutri] < other.__nutri_content[nutri]
        else:
            return False

    def __hash__(self) -> int:
       return hash(self.id)



    @property
    def id(self) -> int:
        return self.__recipe_id

    @property
    def calories(self) -> float:
        return self.__nutri_content["calories"]

    @property
    def fat(self) -> float:
        return self.__nutri_content["fat"]

    @property
    def saturated_fat(self) -> float:
        return self.__nutri_content["saturated_fat"]

    @property
    def cholesterol(self) -> float:
        return self.__nutri_content["cholesterol"]

    @property
    def sodium(self) -> float:
        return self.__nutri_content["sodium"]

    @property
    def carbohydrates(self) -> float:
        return self.__nutri_content["carbohydrates"]

    @property
    def fiber(self) -> float:
        return self.__nutri_content["fiber"]

    @property
    def sugar(self) -> float:
        return self.__nutri_content["sugar"]

    @property
    def protein(self) -> float:
        return self.__nutri_content["protein"]