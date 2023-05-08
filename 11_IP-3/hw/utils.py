
class Positon:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        res = f"""Positon(x={self.x}, y={self.y})"""
        return res