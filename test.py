import string
import random
import time

for i in range(0,1000):
    random_digit = int(''.join(random.choice(string.digits) for i in range(2)))
    print ( ''.join(random.choice(string.ascii_lowercase) for i in range(random_digit)) )
    time.sleep(random.choice([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]))