import logging

from config import settings
from config.celery_settings import app
from main.backend import SheetClient
from main.models import DefaultRate
from main.utils.get_rate_from_cbr import get_rate_from_cbr
from main.utils.save_bids_in_db import save_bids_in_db

logger = logging.getLogger('task')


@app.task(max_retries=1)
def update_rates_from_cbr():
    logger.info(f'update_rates start')
    try:
        rates = DefaultRate.objects.all()
        for rate in rates:
            value = get_rate_from_cbr(rate.title)
            if value:
                rate.value = float(value.replace(',', '.'))
                rate.save(update_fields=['value',])

    except Exception as e:
        logger.exception(f'update_rates error: {e}')

    logger.info('update_rates done')


@app.task(max_retries=1)
def get_data_from_gs_save_in_db():
    logger.info(f'get_data_from_gs start')
    try:
        client = SheetClient()
        values = client.get_values(settings.SPREAD_SHEET_NAME, settings.SHEET_NAME)
        save_bids_in_db(values[1:])
    except Exception as e:
        logger.exception(f'update_rates error: {e}')

    logger.info('get_data_from_gs done')
