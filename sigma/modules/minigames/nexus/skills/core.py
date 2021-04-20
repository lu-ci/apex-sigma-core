import abc
import secrets

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

    def add_skill(self, skill: 'Skill'):
        exists = False
        for skl in self.skills:
            if skl.name == skill.name:
                exists = True
                break
        if not exists:
            self.skills.append(skill)

    def as_dict(self) -> dict:
        data = {}
        for skill in self.skills:
            data.update({skill.name: skill})
        return data

    @staticmethod
    def roll_upgrade(uid: int, attempts: int) -> bool:
        upgraded = False
        triggers = []
        nice_indexes = [6, 9]
        for ni in nice_indexes:
            num = int(str(uid)[ni])
            triggers.append(num)
        for _ in range(attempts):
            roll = secrets.randbelow(50)
            if roll == sum(triggers):
                upgraded = True
                break
        return upgraded

    async def trigger(self, db, msg, name, attempts=1):
        skill: 'Skill' = self.as_dict().get(name)
        upped = self.roll_upgrade(msg.author.id, attempts)
        if upped or True:
            sin = await skill.load(db, msg.author.id)
            leveled = sin.leveled_up(sin.points, sin.points + 1)
            sin.points += 1
            await sin.save(db, msg.author.id)
            if leveled:
                # noinspection PyBroadException
                try:
                    await msg.add_reaction('🆙')
                except Exception:
                    pass


class Skill(abc.ABC):
    def __init__(self, name: str, level_step: float, step_mod: float, max_level: int):
        self.name = name
        self.level_step = level_step
        self.step_mod = step_mod
        self.max_level = max_level

    def points_needed(self, level: int) -> float:
        return self.level_step + (1 + ((level ** 2) * self.step_mod))

    def total_needed(self, level: int) -> float:
        pts = 0
        for lv in range(level):
            pts += self.points_needed(lv)
        return pts

    def level(self, points: int) -> int:
        level = 0
        needed = 0
        first_level = self.points_needed(level)
        if points >= first_level:
            while needed <= points:
                needed += self.points_needed(level)
                if needed <= points:
                    level += 1
                else:
                    break
        if level > self.max_level:
            level = self.max_level
        return level

    def effect(self) -> object:
        raise NotImplemented

    async def load(self, db, uid: int) -> 'SkillInstance':
        skills = await db.get_profile(uid, 'skills') or {}
        points = skills.get(self.name) or 0
        return SkillInstance(self, points)


class SkillInstance(abc.ABC):
    def __init__(self, skill: Skill, points: int):
        self.skill = skill
        self.points = points

    def level(self) -> int:
        return self.skill.level(self.points)

    def progress(self) -> float:
        level = self.level()
        pts = self.skill.total_needed(level)
        upper = self.skill.points_needed(level + 1)
        prog = (self.points - pts) / upper
        if prog > 1:
            prog = 1
        return prog

    def leveled_up(self, old: int, new: int) -> bool:
        old_lv = self.skill.level(old)
        new_lv = self.skill.level(new)
        return old_lv != new_lv

    async def save(self, db, uid: int):
        skills = await db.get_profile(uid, 'skills') or {}
        skills.update({self.skill.name: self.points})
        await db.set_profile(uid, 'skills', skills)
