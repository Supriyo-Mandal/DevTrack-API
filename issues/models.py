from abc import ABC, abstractmethod


class BaseEntity(ABC):
    @abstractmethod
    def validate(self):
        pass

    def to_dict(self):
        return {key: value for key, value in self.__dict__.items()}


class Reporter(BaseEntity):
    def __init__(self, id, name, email, team):
        self.id = int(id)
        self.name = name
        self.email = email
        self.team = team

    def validate(self):
        if not self.name or not self.name.strip():
            raise ValueError('Name cannot be empty')
        if '@' not in self.email or not self.email.strip():
            raise ValueError('Invalid email')


class Issue(BaseEntity):
    VALID_STATUSES = {'open', 'in_progress', 'resolved', 'closed'}
    VALID_PRIORITIES = {'low', 'medium', 'high', 'critical'}

    def __init__(self, id, title, description, status, priority, reporter_id, created_at=None):
        self.id = int(id)
        self.title = title
        self.description = description
        self.status = status
        self.priority = priority
        self.reporter_id = int(reporter_id)
        self.created_at = created_at or __import__('datetime').datetime.now().isoformat()

    def validate(self):
        if not self.title or not self.title.strip():
            raise ValueError('Title cannot be empty')
        if self.status not in self.VALID_STATUSES:
            raise ValueError('Invalid status')
        if self.priority not in self.VALID_PRIORITIES:
            raise ValueError('Invalid priority')

    def describe(self):
        return f"{self.title} [{self.priority}]"


class CriticalIssue(Issue):
    def describe(self):
        return f"[URGENT] {self.title} — needs immediate attention"


class LowPriorityIssue(Issue):
    def describe(self):
        return f"{self.title} — low priority, handle when free"
