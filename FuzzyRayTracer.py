import math

class FuzzyRayTracer:
    def __init__(self, points, x, y, r, fov = 360, numRays = 60):
        self.points = points
        self.x = x
        self.y = y
        self.r = r
        self.fov = fov
        self.numRays = numRays

    def trace(self):
        angles = []
        for point in self.points:
            delta1 = math.atan2((point[1] - self.y), (point[0] - self.x))
            delta2 = self.r / 180 * math.pi
            deltadelta = 360 - (delta1 - delta2) * 180 / math.pi
            deltadelta %= 360
            if deltadelta > 180:
                deltadelta -= 360
            angles.append((deltadelta, math.sqrt((point[1] - self.y)**2 + (point[1] - self.y) ** 2), point[2]))
        # print angles
        rayIncr = self.fov / self.numRays
        rays = [0] * (self.numRays * 2);
        # print rays
        for rayNum in range(self.numRays):
            rayngle = rayIncr * rayNum - (self.fov / 2)
            # print rayngle
            for angle in angles:
                if abs(angle[0] - rayngle) < rayIncr / 2:
                    idx = rayNum if angle[2] > 0 else rayNum + self.numRays
                    rays[idx] = 1 - max(angle[1] / 300.0, 1);
        return rays
