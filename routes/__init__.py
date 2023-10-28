from .auth0 import auth0
from .capital_one import capital_one
from .tasks import tasks

ALL = [auth0, capital_one, tasks]

__all__ = ALL