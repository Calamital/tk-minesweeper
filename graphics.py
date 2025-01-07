class color():
    @staticmethod
    def _itoh(i:int):
        H0:int = i//16
        H1:int = i%16
        return (chr(65+H0%10) if H0>9 else str(H0))+(chr(65+H1%10) if H1>9 else str(H1))
    @staticmethod
    def rgbtohex(rgb:tuple):
        return "#"+color._itoh(rgb[0])+color._itoh(rgb[1])+color._itoh(rgb[2])