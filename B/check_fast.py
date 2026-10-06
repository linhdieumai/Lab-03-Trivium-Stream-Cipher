"""
Before using fast_cube.py, confirm it agrees with YOUR cube_sum on small cubes.
    python3 check_fast.py
"""
import random
from zero_sum import cube_sum
from fast_cube import fast_cube_sum
rng = random.Random(1)
for trial in range(10):
    k = rng.randint(1, 5)
    cube = sorted(rng.sample(range(1, 81), k))
    R = rng.choice([100, 300, 500, 650])
    key = [rng.getrandbits(1) for _ in range(80)]
    a, b = cube_sum(key, cube, R), fast_cube_sum(key, cube, R)
    print(f"cube {cube}, R={R}: yours={a} fast={b}", "OK" if a == b else "MISMATCH")
