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


class Char:
    """A single character that is part of an Image"""

    def __init__(self, x, y, char):

        self.x = x
        self.y = y
        self.char = char  # string


class Image:
    """Something displayed on the canvas"""

    def __init__(self, canvas, x, y, chars):
        
        self.canvas = canvas
        self.x = x
        self.y = y
        self.chars = chars

    def render(self):
        """Alter canvas display to update current state of self."""
        # canvas_x means location of char on the canvas

        for char in self.chars:
            
            # replace all previous chars with spaces on canvas

            canvas_x = self.x + char.x
            canvas_y = self.y + char.y

            self.canvas.replace(canvas_x, canvas_y, char.char)


