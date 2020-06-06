from django_cron import CronJobBase, Schedule
from news.models import Post


class ResetUpvotesCronJob(CronJobBase):
    """This function resets amount of upvotes for all news every 24 hour"""

    RUN_EVERY_MINS = 1440

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = "news_board_API.reset_upvotes"

    def do(self):
        """This function filters all the news upvoted and resets amount of upvotes for them"""
        Post.objects.filter(amount_of_upvotes__gt=0).update(
            amount_of_upvotes=0
        )