class ItemNotFoundException(Exception):
    pass

class ColorNotFoundException(ItemNotFoundException):
    pass

class SizeNotFoundException(ItemNotFoundException):
    pass

class SkuNotFoundException(ItemNotFoundException):
    pass

class UnknownCommandError(Exception):
    pass


