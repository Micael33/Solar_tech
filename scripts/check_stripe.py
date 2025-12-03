import os
import json
from pathlib import Path
import sys

# Ensure project root is current working directory and on sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
os.chdir(str(BASE_DIR))
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE","solar_store.settings")
import django
django.setup()
from django.conf import settings

print("--- Django settings read ---")
print("STRIPE_SECRET_KEY =", settings.STRIPE_SECRET_KEY)

print('\n--- Testing Stripe API using settings STRIPE_SECRET_KEY ---')
try:
    import stripe
    stripe.api_key = settings.STRIPE_SECRET_KEY
    balance = stripe.Balance.retrieve()
    print('Stripe API call successful. Balance keys:', list(balance.keys()))
except Exception as e:
    print('Stripe API error:', repr(e))
