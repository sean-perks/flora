def num_in_range(value, ge, gt, le, lt):
    if ge is not None and value < ge:
        return False
    if gt is not None and value <= gt:
        return False
    if le is not None and value > le:
        return False
    if lt is not None and value >= lt:
        return False
    return True


def input_int(prompt="Enter an integer: ", error="Invalid!",
              ge=None, gt=None, le=None, lt=None):
    while True:
        try:
            val_string = input(prompt)
            val_int = int(val_string)
            if num_in_range(val_int, ge, gt, le, lt):
                return val_int
            print(error)
        except ValueError:
            print(error)


# An input_float function that asks the user to type in a decimal number.
def input_float(prompt="Enter a float: ", error="Invalid!",
                ge=None, gt=None, le=None, lt=None):
    while True:
        try:
            val_string = input(prompt)
            val_float = float(val_string)
            if num_in_range(val_float, ge, gt, le, lt):
                return val_float
            print(error)
        except ValueError:
            print(error)


# An input_string function that asks the user to type in a piece of text.
def input_string(
        prompt="Input a string: ",
        error="Invalid. Must not be empty.",
        valid=lambda s: len(s) > 0
):
    while True:
        try:
            val = input(prompt)
            if valid(val):
                return val
            print(error)
        except ValueError:
            print(error)


# function to check yes/no
def y_n(
        prompt="Enter yes or no (y/n): ",
        error="Invalid, try again."
):
    while True:
        try:
            yn = input(prompt).lower()
            if yn in ['y', 'yes', 'yep', 'yeppers']:
                return True
            if yn in ['n', 'no', 'nope', 'hell no']:
                return False
            print(error)
        except ValueError:
            print(error)


def select_item(
        prompt="Enter yes or no: ",
        error="Answer must be yes or no!",
        choices=["y", "n"],
        map=None
):
    value_dict = {}
    for choice in choices:
        value_dict[choice.lower()] = choice
    if map is not None:
        for key in map:
            value_dict[key.lower()] = map[key]
    while True:
        val = input(prompt).lower()
        if val in value_dict:
            return value_dict[val]
        print(error)


def input_item(type="int", *args, **kwargs):
    if type == "int":
        return input_int(*args, **kwargs)
    elif type == "y_or_n":
        return y_n(*args, **kwargs)
    elif type == "string":
        return input_string(*args, **kwargs)
    elif type == "select":
        return select_item(*args, **kwargs)
    else:
        print("Error! Unknown type", type)



