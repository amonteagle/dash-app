bind = "0.0.0.0:8050"       # gunicorn listens on all interfaces
workers = 4                 # or `multiprocessing.cpu_count() * 2 + 1`
threads = 2                 # inexpensive for Dash apps
timeout = 120               # seconds before killing hung workers
