class AddPageFailedException(Exception):
    """
    添加书页失败
    """

    def __init__(self) -> None:
        super().__init__("Failed to add Page")
