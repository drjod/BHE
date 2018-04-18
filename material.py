


class Material:
    def __init__(self, capacity, conductivity):
        self.capacity = capacity
        self.conductivity = conductivity



class MaterialSet:
    def __init__(self, numberOfLayers):
        self.fluid = Material(4200000., 1.)
        self.filling = Material(4000000., 2.)
        self.groundList = [Material(400000.,2)] * numberOfLayers
