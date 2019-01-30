import multiprocessing
from src import settings

bind = '{host}:{port}'.format(host=settings.HOST, port=settings.PORT)
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'meinheld.gmeinheld.MeinheldWorker'

print(f'Workers: {workers}')
