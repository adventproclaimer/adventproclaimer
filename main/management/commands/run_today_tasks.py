import time
import ast
import logging
from datetime import date
from django.utils import timezone
from django.core.management.base import BaseCommand
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from celery import current_app

# --------------------
# Terminal logging
# --------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Run today's django-celery-beat tasks sequentially with 1-minute spacing"

    def handle(self, *args, **options):
        today = timezone.now().date()
        start_time = timezone.now()

        logger.info("Starting Celery Beat backfill run")
        logger.info("Execution date: %s", today)

        tasks = self._get_tasks_for_today(today)

        if not tasks:
            logger.warning("No enabled Celery Beat tasks scheduled for today")
            return

        logger.info("Found %d task(s) to run today", len(tasks))

        for i, task in enumerate(tasks, start=1):
            logger.info("(%d/%d) Running task: %s", i, len(tasks), task.name)
            self._run_task(task)

            if i < len(tasks):
                logger.info("Sleeping for 60 seconds before next task")
                time.sleep(60)

        duration = (timezone.now() - start_time).total_seconds()
        logger.info("All tasks completed in %.2f seconds", duration)

    # --------------------
    # Helpers
    # --------------------

    def _get_tasks_for_today(self, today: date):
        results = []

        for task in PeriodicTask.objects.filter(enabled=True).select_related("crontab"):
            if not task.crontab:
                continue

            crontab: CrontabSchedule = task.crontab

            if self._matches_today(crontab, today):
                results.append(task)

        return results

    def _matches_today(self, crontab: CrontabSchedule, today: date):
        return (
            crontab.day_of_month in ("*", str(today.day))
            and crontab.month_of_year in ("*", str(today.month))
        )

    def _run_task(self, task: PeriodicTask):
        try:
            celery_task = current_app.tasks.get(task.task)

            if not celery_task:
                logger.error("Task not registered in Celery: %s", task.task)
                return

            args = ast.literal_eval(task.args or "[]")
            kwargs = ast.literal_eval(task.kwargs or "{}")

            logger.info("Dispatching Celery task: %s", task.task)
            celery_task.apply_async(args=args, kwargs=kwargs)

            logger.info("Successfully dispatched: %s", task.name)

        except Exception as e:
            logger.exception("Error while running task %s: %s", task.name, e)
