from ui.Species import Species


class TwoFactorSpecies(Species):
    __two_f_type = ""
    __two_f_pin = 0

    def __init__(self, title, url, username, password, date_pass_change, two_f_type, two_f_pin):
        # super allows assigning from the parent __init__
        super().__init__(title, url, username, password, date_pass_change)
        # TwoFactorAccount specific properties
        self.__two_f_type = two_f_type
        self.__two_f_pin = two_f_pin

    def __str__(self):
        return super().__str__() + f", TF type: {self.__two_f_type}, TF pin: {self.__two_f_pin}"
