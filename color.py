from colorama import init, Fore, Back

init(autoreset=False)


class Color(object):
    """
    用于美化打印内容
    """
    #  前景色:红色  背景色:默认
    @classmethod
    def red(cls, s):
        return Fore.RED + s + Fore.RESET

    @classmethod
    #  前景色:绿色  背景色:默认
    def green(cls, s):
        return Fore.GREEN + s + Fore.RESET

    @classmethod
    #  前景色:黄色  背景色:默认
    def yellow(cls, s):
        return Fore.YELLOW + s + Fore.RESET

    #  前景色:蓝色  背景色:默认
    @classmethod
    def blue(cls, s):
        return Fore.BLUE + s + Fore.RESET

    #  前景色:洋红色  背景色:默认
    @classmethod
    def magenta(cls, s):
        return Fore.MAGENTA + s + Fore.RESET

    #  前景色:青色  背景色:默认
    @classmethod
    def cyan(cls, s):
        return Fore.CYAN + s + Fore.RESET

    #  前景色:白色  背景色:默认
    @classmethod
    def white(cls, s):
        return Fore.WHITE + s + Fore.RESET

    #  前景色:黑色  背景色:默认
    @classmethod
    def black(cls, s):
        return Fore.BLACK

    #  前景色:白色  背景色:绿色
    @classmethod
    def white_green(cls, s):
        return Fore.WHITE + Back.GREEN + s + Fore.RESET + Back.RESET
