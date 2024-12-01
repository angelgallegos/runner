from app.fly import Fly
from app.fly import Obstacle
from app.stages import Stage


class ObstacleFactory:
    def __init__(self):
        pass

    def create(self, obstacle_type: str, stage: Stage):
        if obstacle_type == 'fly':
            return Fly(stage)
        else:
            return Obstacle(stage)
