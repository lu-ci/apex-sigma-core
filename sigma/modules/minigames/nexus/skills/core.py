import abc

SC_INSTANCE = None

class SkillCore(abc.ABC):
    def __init__(self):
        self.skills: [Skill] = []

    @staticmethod
    def instance() -> 'SkillCore':
        global SC_INSTANCE
        if SC_INSTANCE is None:
            SC_INSTANCE = SkillCore()
        return SC_INSTANCE

    def as_dict(self) -> dict:
        data = {}
        for skill in self.skills:
            data.update({skill.name: skill})
        return data

    def roll_upgrade(self, uid: int, attempts: int) -> bool:
        triggers = []
        nice_indexes = [6, 9]



class Skill(abc.ABC):
    def __init__(self, name: str, level_step: float, step_mod: float, max_level: int):
        self.name = name
        self.level_step = level_step
        self.step_mod = step_mod
        self.max_level = max_level

    def level(self, points: int) -> int:
        pass  # TODO


class SkillInstance(abc.ABC):
    def __init__(self, skill: Skill, points: int):
        self.skill = skill
        self.points = points

    def level(self) -> int:
        return self.skill.level(self.points)

    def leveled_up(self, old: int, new: int) -> bool:
        old_lv = self.skill.level(old)
        new_lv = self.skill.level(new)
        return old_lv != new_lv
