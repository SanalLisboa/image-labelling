
class CustomImageLabellingException(Exception):
    def __init__(self, message):

        self.message = message

        super().__init__(message)


class ImageAlreadyExists(CustomImageLabellingException):
    def __init__(self, message):

        super().__init__(message)


class ImageDosentExist(CustomImageLabellingException):
    def __init__(self, message):

        super().__init__(message)


class LabelDoesntExist(CustomImageLabellingException):
    def __init__(self, message):

        super().__init__(message)


class UnauthorizedAction(CustomImageLabellingException):
    def __init__(self, message):

        super().__init__()
