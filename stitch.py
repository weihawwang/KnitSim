class Stitch:
    def __init__(self, address: list[int, int], size: int = 10, color: str = "black"):
        """
        Represents a single stitch in the knitting simulation.

        :param address: A list containing [row, col] position of the stitch.
        :param size: Displayed size of the stitch (default: 10).
        :param color: Displayed color of the stitch (default: black).
        """
        self.address = address  # [row, col]
        self.size = size
        self.color = color

    def __repr__(self):
        return f"Stitch(address={self.address}, size={self.size}, color='{self.color}')"

    def change_color(self, new_color: str):
        """Change the color of the stitch."""
        self.color = new_color

    def resize(self, new_size: int):
        """Change the size of the stitch."""
        self.size = new_size
