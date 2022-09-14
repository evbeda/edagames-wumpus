class invalidMoveException(Exception):
    pass


class moveToYourOwnCharPositionException(invalidMoveException):
    pass


class notYourCharacterException(invalidMoveException):
    pass


class noPossibleMoveException(invalidMoveException):
    pass


class noArrowsAvailableException(invalidMoveException):
    pass


class friendlyFireException(invalidMoveException):
    pass


class shootOutOfBoundsException(invalidMoveException):
    pass