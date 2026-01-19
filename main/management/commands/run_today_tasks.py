import time
import ast
import logging
from datetime import date
from django.utils import timezone
from django.core.management.base import BaseCommand
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from celery import current_app

# --------------------------------------------------
# Terminal logging
# --------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Run today's django-celery-beat tasks sequentially with 1-minute spacing"

    def handle(self, *args, **options):
        today = timezone.localdate()
        start_time = timezone.now()

        logger.info("================================================")
        logger.info("Starting Celery Beat sequential run")
        logger.info("Execution date: %s", today)
        logger.info("================================================")

        tasks = self._get_tasks_for_today(today)

        if not tasks:
            logger.warning("No enabled Celery Beat tasks scheduled for today")
            return

        logger.info("Found %d task(s) scheduled for today", len(tasks))

        for index, task in enumerate(tasks, start=1):
            scheduled_time = self._get_task_time(task)

            logger.info(
                "[%d/%d] Executing task: %s (scheduled ~ %02d:%02d)",
                index,
                len(tasks),
                task.name,
                scheduled_time[0],
                scheduled_time[1],
            )

            self._run_task(task)

            if index < len(tasks):
                logger.info("Sleeping 60 seconds before next task...")
                time.sleep(60)

        duration = (timezone.now() - start_time).total_seconds()
        logger.info("================================================")
        logger.info("All tasks completed in %.2f seconds", duration)
        logger.info("================================================")

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    def _get_tasks_for_today(self, today: date):
        results = []

        queryset = (
            PeriodicTask.objects
            .filter(enabled=True)
            .select_related("crontab")
        )

        for task in queryset:
            if not task.crontab:
                continue

            if self._matches_today(task.crontab, today):
                results.append(task)

        # Sort tasks from earliest → latest
        results.sort(key=self._get_task_time)

        return results

    def _matches_today(self, crontab: CrontabSchedule, today: date):
        return (
            self._cron_matches(crontab.day_of_month, today.day)
            and self._cron_matches(crontab.month_of_year, today.month)
        )

    def _cron_matches(self, field: str, value: int):
        if field == "*":
            return True

        values = set()
        for part in field.split(","):
            if "-" in part:
                start, end = map(int, part.split("-"))
                values.update(range(start, end + 1))
            else:
                values.add(int(part))

        return value in values

    def _get_task_time(self, task: PeriodicTask):
        """
        Return a sortable (hour, minute) tuple.
        '*' resolves to earliest possible time.
        """
        crontab = task.crontab

        def parse(field, max_value):
            if field == "*":
                return 0

            values = []
            for part in field.split(","):
                if "-" in part:
                    start, end = map(int, part.split("-"))
                    values.extend(range(start, end + 1))
                elif part.startswith("*/"):
                    step = int(part[2:])
                    values.extend(range(0, max_value + 1, step))
                else:
                    values.append(int(part))

            return min(values) if values else 0

        hour = parse(crontab.hour, 23)
        minute = parse(crontab.minute, 59)

        return (hour, minute)

    def _run_task(self, task: PeriodicTask):
        try:
            celery_task = current_app.tasks.get(task.task)

            if not celery_task:
                logger.error("Celery task not registered: %s", task.task)
                return

            args = ast.literal_eval(task.args or "[]")
            kwargs = ast.literal_eval(task.kwargs or "{}")

            logger.info("Dispatching Celery task: %s", task.task)
            celery_task.apply_async(args=args, kwargs=kwargs)

            logger.info("Task dispatched successfully: %s", task.name)

        except Exception:
            logger.exception("Failed to execute task: %s", task.name)
