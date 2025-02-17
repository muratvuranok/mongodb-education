class StringExtensions:
    """
    String Extension Functions
    """

    @staticmethod
    def to_username(text: str) -> str:
        """
        Convert text to username format, all lowercase and no spaces
        """
        return (
            text.lower()
            .replace(" ", "")
            .replace("ç", "c")
            .replace("ğ", "g")
            .replace("ı", "i")
            .replace("ö", "o")
            .replace("ş", "s")
            .replace("ü", "u")
        )
