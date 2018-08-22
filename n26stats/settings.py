import os

# Environment.
DEVELOPMENT = 'development'
TESTING = 'testing'
PRODUCTION = 'production'
ENVIRONMENT = os.getenv('ENVIRONMENT') or DEVELOPMENT
VALID_ENVIRONMENTS = [DEVELOPMENT, TESTING, PRODUCTION]
if ENVIRONMENT not in VALID_ENVIRONMENTS:
    raise Exception(f'Environment "{ENVIRONMENT}" not in {VALID_ENVIRONMENTS}')
