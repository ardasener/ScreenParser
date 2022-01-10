class ScreenObject:
    def __init__(self, x1, y1, x2, y2, confidence=0.1, text=""):
        # Coordinates for the bounding box
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        # Float from 0 to 1
        # High confidence indicates the object
        # is more likely to be a correct detection
        self.confidence = confidence

        # Text detected by tesseract
        # If empty then the object contains no text
        self.text = text

        self.dists = []

    def get_center(self):
      return int(self.x1 + self.width()/2), int(self.y1 + self.height()/2)

    def get_xyxy(self):
        return self.x1, self.y1, self.x2, self.y2

    def get_xywh(self):
        return self.x1, self.y1, self.width(), self.height()

    def width(self):
        return self.x2 - self.x1

    def height(self):
        return self.y2 - self.y1

    def area(self):
        return self.width() * self.height()

    def horizontal_distance(self,other):
        self_center = int(self.x1 + self.width()/2)
        other_center = int(other.x1 + other.width()/2)
        return abs(self_center-other_center)

    def vertical_distance(self,other):
        self_center = int(self.y1 + self.height()/2)
        other_center = int(other.y1 + other.height()/2)
        return abs(self_center-other_center)

    def __str__(self):
        s = "<ScreenObject x1={} y1={} x2={} y2={} text='{}' confidence={} />".format(
            self.x1, self.y1, self.x2, self.y2, self.text, self.confidence)
        return s

    # Returns the intersection area of this and the other object
    def intersection(self, other):
        max_x1 = max(self.x1, other.x1)
        min_x2 = min(self.x2, other.x2)

        x_diff = min_x2 - max_x1

        if x_diff < 0:
            return 0

        max_y1 = max(self.y1, other.y1)
        min_y2 = min(self.y2, other.y2)

        y_diff = min_y2 - max_y1

        if y_diff < 0:
            return 0

        return x_diff * y_diff

    def merge(self, other):
      if other.text != "":
        if self.x1 < other.x1:
          self.text = self.text + other.text
        else:
          self.text = other.text + self.text

      self.x1 = min(self.x1, other.x1)
      self.x2 = max(self.x2, other.x2)
      self.y1 = min(self.y1, other.y1)
      self.y2 = max(self.y2, other.y2)

      self.confidence = max(self.confidence, other.confidence)

    def __str__(self):
      return "ScreenObject {} ({} {}) ({} {})".format(self.text,self.x1,self.y1,self.x2,self.y2)