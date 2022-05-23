from datetime import datetime
from decimal import Decimal

from main.models import Bid


def save_bids_in_db(values_list):
    bid_ids = list(Bid.objects.all().values_list('bid_id', flat=True))
    for row in values_list:
        try:
            raw_bid = {
                'number': int(row[0]),
                'bid_id': int(row[1]),
                'price_usd': Decimal(row[2]),
                'delivery_time': datetime.strptime(row[-1], '%d.%m.%Y')
            }
            bid, created = Bid.objects.update_or_create(bid_id=raw_bid['bid_id'], defaults=raw_bid)
            if not created:
                bid_ids.remove(bid.bid_id)
        except ValueError:
            pass
    if bid_ids:
        Bid.objects.filter(bid_id__in=bid_ids).delete()
