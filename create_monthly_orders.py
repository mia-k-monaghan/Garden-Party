import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garden_party.settings')

import django
django.setup()

from django.contrib.auth import get_user_model
from djstripe.models import Subscription
from core.models import MonthlyOrder

users = get_user_model()

def create_orders():
    for order in users.objects.all():
        if order.has_active_subscription:
            o = MonthlyOrder.objects.get_or_create(user=order)
            print('YES')
        else:
            print("no orders")

create_orders()
