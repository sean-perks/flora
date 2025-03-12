class Species:
    __scientific_name = []
    __spell_checked_species = []
    __symbol = []
    __common_name = []
    __synonym = []

# constructor to initialize class properties
    def __init__(self, scientific_name, spell_checked_species, common_name, symbol, synonym):
        self.__scientific_name = scientific_name
        self.__spell_checked_species = spell_checked_species
        self.__symbol = symbol
        self.__common_name = common_name
        self.__synonym = synonym

    # custom override for printing class objects
    def __str__(self):
        return f"{self.__scientific_name}, {self.__symbol}, {self.__common_name}"

    def get_scientific_name(self):
        return self.__scientific_name

    def get_spell_checked_species(self):
        return self.__spell_checked_species

    def get_symbol(self):
        return self.__symbol

    def get_common_name(self):
        return self.__common_name

    def set_species_list(self, species_list):
        self.__scientific_name = species_list

    def set_spell_checked_species(self, species_list):
        self.__spell_checked_species = species_list


