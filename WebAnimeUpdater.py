import datetime
import workers

from configs import EPISODE_SEARCH_FREQUENCY
from commons import logger as log
from tornadoApp import TornadoApp
from scheduler import Scheduler

episodeSearchScheduler = Scheduler(
    workers.SearchEpisodesWorker(),
    run_delay=datetime.timedelta(minutes=1),
    cycle_time=datetime.timedelta(minutes=EPISODE_SEARCH_FREQUENCY),
    thread_name="EPISODESEARCH"
)

if __name__ == "__main__":
    log.info("Starting episodeSearchScheduler...")
    # start the daily search scheduler
    episodeSearchScheduler.enable = True
    episodeSearchScheduler.start()
    log.info("Started episodeSearchScheduler.")

    log.info("Starting TornadoApp...")
    # start tornado WebApp
    webapp = TornadoApp()
    webapp.start()

