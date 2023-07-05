class Profile:
    def __init__(self, name, h, b, tw, tf, r, A, m):
        self.name = name
        self.h = h          #mm
        self.b = b          #mm
        self.tw = tw        #mm
        self.tf = tf        #mm
        self.r = r          #mm
        self.A = A          #cm2
        self.m = m          #kg/m

HEA140 = Profile("HEA140", 133, 140, 5.5, 8.5, 12, 31.40, 24.7)