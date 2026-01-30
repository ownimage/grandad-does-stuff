from ownimage.font_generator.birdfont_reader import BirdfontReader
from ownimage.font_generator.blackletter import Blackletter

br = BirdfontReader("cour.birdfont")
br.load()
# x = br.get_paths_by_unicode("a")
# print(f"Result: {x}")
#
# paths = [
#        "S 8.23223,22.92893 L 8.23223,3.53553 L 11.76777,7.07107 L 11.76777,26.46447 L 8.23223,22.92893",
#        "S 8.23223,3.53553 L 11.76777,-0.00000 L 15.30330,3.53553 L 11.76777,7.07107 L 8.23223,3.53553",
#        "S 11.76777,26.46447 L 15.30330,22.92893 L 18.83883,26.46447 L 15.30330,30.00000 L 11.76777,26.46447",
#        "S 15.30330,22.92893 L 15.30330,3.53553 L 18.83883,7.07107 L 18.83883,26.46447 L 15.30330,22.92893",
#        "S 15.30330,3.53553 L 18.83883,-0.00000 L 22.37437,3.53553 L 18.83883,7.07107 L 15.30330,3.53553"
# ]

blackletter = Blackletter(.5, 0, 3, 7)
# print(blackletter.birdfont_path('a', 10))

br.replace_paths_by_unicode("a", blackletter.birdfont_path('a', 10))
br.replace_paths_by_unicode("b", blackletter.birdfont_path('b', 10))
br.save()
