from .modules import queries

def esmac():
    print queries.esmacfinder.run()

def bromac():
    print queries.bromacfinder.run()

test = esmac()
test2 = bromac()