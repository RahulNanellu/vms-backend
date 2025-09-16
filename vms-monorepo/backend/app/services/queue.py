from rq import Queue
from redis import Redis
from ..core.config import settings

redis = Redis.from_url(settings.REDIS_URL)
q_high = Queue("ptt_high", connection=redis, default_timeout=300)
q_norm = Queue("ptt_norm", connection=redis, default_timeout=300)
q_low  = Queue("ptt_low",  connection=redis, default_timeout=300)

def enqueue_ptt(priority: str, job, *args, **kwargs):
    if priority == "HIGH":
        return q_high.enqueue(job, *args, **kwargs)
    if priority == "LOW":
        return q_low.enqueue(job, *args, **kwargs)
    return q_norm.enqueue(job, *args, **kwargs)
