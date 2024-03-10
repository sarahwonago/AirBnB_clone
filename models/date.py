class Base:
    def __init__(self, *args):
        
        print("Hello world")

my_name = Base()
my_name.location = "Kenya"
print("{} I am from {}".format(my_name, my_name.location))
