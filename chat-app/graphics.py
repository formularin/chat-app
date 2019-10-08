class Canvas:
    """Represents string that is displayed to the screen with each frame"""

    def __init__(self, height, width):
        self.grid = [["#" for _ in range(width)] for _ in range(height)]

    def replace(self, x, y, char):
        """
        Replaces char in certain location of self.grid

        (0, 0) is bottom-left corner.
        Y increases in upward direction, X to the right.
        """
        row_index = (len(self.grid) - 1) - y
        self.grid[row_index][x] = char


    @property
    def display(self):
        rows = ["".join(row) for row in self.grid]
        return '\n'.join(rows)