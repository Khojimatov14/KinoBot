from loader import dp
from .throttling import ThrottlingMiddleware
from .checksub import Subscription


dp.update.middleware(ThrottlingMiddleware())
dp.update.middleware(Subscription())
