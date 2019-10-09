class Canvas:
    """Represents string that is displayed to the screen with each frame"""

    def __init__(self, height, width):
        self.grid = [[" " for _ in range(width)] for _ in range(height)]

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
        rows = ["".join(row) for row in self.grid][::-1]
        return '\n'.join(rows)


class Char:
    """A single character that is part of an Image"""

    def __init__(self, x, y, char):

        self.x = x
        self.y = y
        if len(char) == 1:
            self.char = char
        else:
            raise ValueError("Char object can only represent one char.")


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


class InputLine(Image):
    """
    Represents a line where if you type, it will record what was typed
    
    Renders on canvas arg and
    if echo is False, will not render typed chars on window.
    """

    def __init__(self, canvas, prompt, echo=True):
        
        self.prompt_length = len(prompt)
        self.cursor_index = self.prompt_length
        self.echo = echo
        self.submitted = False
        self.inputted_chars = []

        y = len(canvas.grid) - 1
        prompt_chars = [Char(i, 0, char) for i, char in enumerate(prompt)]
        input_chars = [Char(i, 0, " ") for i in range(self.prompt_length, len(canvas.grid[-1]))]
        chars = prompt_chars + input_chars

        Image.__init__(self, canvas, 0, y, chars)

    @property
    def value(self):
        return ''.join(self.inputted_chars)

    def _del_char(self):
        """Removes last char from input field"""
        if self.cursor_index > self.prompt_length:
            self.chars[self.cursor_index] = Char(self.cursor_index, 0, " ")
            self.cursor_index -= 1
            self.inputted_chars = self.inputted_chars[:-1]

    def type_char(self, char):
        """Adds char to value of input field"""
        if not (char in [-1, 127, 10]):
            try:
                if self.echo:
                    new_char = chr(char)
                else:
                    new_char = "*"
                self.chars[self.cursor_index] = Char(self.cursor_index, 0, new_char)
                self.cursor_index += 1
                self.inputted_chars.append(chr(char))
            except Exception:
                pass
        elif char == 127:
            self._del_char()
        elif char == 10:
            self.submitted = True
            len_chars = len(self.chars)
            self.chars = [Char(i, 0, " ") for i in range(len_chars)]
            self.render()


class Cursor(Image):
    """Represents the block character used to represent cursor"""

    def __init__(self, canvas):
        Image.__init__(self, canvas, 0, 0, [Char(0, 0, u"\u2588")])

        self.previous_x = self.x
        self.previous_y = self.y

        self.previous_char = self.chars[0]

    def render(self):
        """
        Override inherited render method because
        this Image can move and has only one char
        """
        self.canvas.replace(
            self.previous_y,
            (len(self.canvas.grid) - 1) - self.previous_x,
            " ")
        self.canvas.replace(
            self.y,
            (len(self.canvas.grid) - 1) - self.x,
            self.chars[0].char)

    def toggle_char(self):
        """Changes from block char to space for blinking effect"""
        new_char = self.previous_char
        old_char = self.chars[0]
        self.chars[0] = new_char
        self.previous_char = old_char

    def move(self, x, y):
        """Moves cursor to (x, y) on the canvas"""

        self.previous_x = self.x
        self.previous_y = self.y

        self.x = x
        self.y = y
