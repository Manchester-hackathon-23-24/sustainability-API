from typing import List
from io import BytesIO

from .constants import USERS, ADMINS, TASK_QUEUE

class User:
    cache = {}
    DEFAULT = {
        "capital_one": None,
        "completed_tasks": [],
        "denied_tasks": []
    }

    @classmethod 
    def __get_cache(cls, user_id: int):
        """Returns a cached object"""
        return cls.cache[user_id] if user_id in cls.cache else None

    def __new__(cls, user_id: int, *args, **kwargs):
        existing = cls.__get_cache(user_id)
        if existing:
            return existing
        return super().__new__(cls)

    def __init__(self, user_id: int):
        if user_id in self.cache:
            return 
        
        self.user_id = user_id

        data = USERS.find_one({'_id': user_id})

        if not data:
            USERS.insert_one({'_id': user_id, **self.DEFAULT})
            data = self.DEFAULT

        self.completed_tasks: List[int] = data['completed_tasks']
        self.denied_tasks: List[int] = data['denied_tasks']

        self.cache[user_id] = self

    @property
    def is_admin(self):
        """Returns whether the user is an admin"""
        return self.user_id in ADMINS

    def add_capital_one_account(self, account_id: str):
        """Adds a capital one account to the user's data"""
        USERS.update_one({'_id': self.user_id}, {'$set': {'capital_one': account_id}})
        self.capital_one = account_id

    def add_completed_task(self, task_id: int):
        """Adds a completed task to the user's data"""
        if task_id in self.denied_tasks: # If the task was previously denied, delete that record
            USERS.update_one({'_id': self.user_id}, {'$pull': {'denied_tasks': task_id}})
            self.denied_tasks.remove(task_id)

        USERS.update_one({'_id': self.user_id}, {'$push': {'completed_tasks': task_id}})
        self.completed_tasks.append(task_id)

    def add_denied_task(self, task_id: int):
        """Adds a denied task to the user's data"""
        if task_id in self.denied_tasks: # If the task is already marked as denied no need to add it again
            return 
        
        USERS.update_one({'_id': self.user_id}, {'$push': {'denied_tasks': task_id}})
        self.denied_tasks.append(task_id)

class TaskQueue:
    """The list of submitted tasks to be approved by an admin"""

    cache = []

    @classmethod
    def __get_cache(cls):
        """Returns a cached object"""
        return cls.cache
    
    def __new__(cls, *args, **kwargs):
        existing = cls.__get_cache()
        if existing:
            return existing
        return super().__new__(cls)
    
    def __init__(self):
        if self.cache:
            return
        
        self.cache = list(TASK_QUEUE.find())

    def add_task(self, task_id: int, user_id: int, task_info: BytesIO):
        """Adds a task to the queue"""
        TASK_QUEUE.insert_one({'_id': task_id, 'user_id': user_id, 'task_info': task_info})
        self.cache.append({'_id': task_id, 'user_id': user_id, 'task_info': task_info})

    
    def approve_task(self, task_id: int, user_id: int):
        """Approves a task"""
        # Save task to approved list in user
        user = User(user_id)
        user.add_completed_task(task_id)

        TASK_QUEUE.delete_one({'_id': task_id})
        self.cache = [task for task in self.cache if task['task_id'] != task_id and task['user_id'] != user_id]

    def deny_task(self, task_id: int, user_id: int):
        """Denies a task"""
        # Save task to denied list in user
        user = User(user_id)
        user.add_denied_task(task_id)

        TASK_QUEUE.delete_one({'_id': task_id})
        self.cache = [task for task in self.cache if task['task_id'] != task_id and task['user_id'] != user_id]

    def get_task_image(self, task_id: int, user_id: int):
        """Returns the image of a task"""
        return [task for task in self.cache if task["user_id"] == user_id and task["task_id"] == task_id]['task_info']
