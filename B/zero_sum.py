"""
Track B (bonus) --- a zero-sum distinguisher on reduced-round Trivium.

Idea. Choose a small set of IV positions, the "cube", e.g. cube = [1, 4, 7].
Run R-round Trivium for EVERY possible value of those IV bits (2^len(cube)
runs; all other IV bits stay 0) and XOR together the first output bit of each
run. This XOR is the "cube sum".

For a truly random cipher, the cube sum would be 0 or 1 at random, changing
from key to key. But if R is small, the cube sum of Trivium is the SAME for
every key (usually 0). That is a distinguisher: an attacker who sees the
output can tell reduced-round Trivium apart from a random stream, without
knowing the key.

Tasks:
  B1  Implement cube_sum and is_constant below.
  B2  For a few cubes, find the largest R where the cube sum is still
      constant (max_rounds does this for you once B1 works).
  B3  (open) Find the cube with the largest R you can. See the handout.

WARNING --- "constant for the keys I tried" is not a proof. With few keys you
may be lucky. Test with at least 50 random keys before you believe a result;
the grader re-tests every claim with many more keys.
"""
import os, random
from trivium import Trivium

def cube_sum(key_bits, cube, R):
    """
    key_bits : list of 80 key bits
    cube     : list of IV positions, numbered 1..80
    R        : number of initialization rounds
    Returns the XOR, over all 2^len(cube) assignments of the cube IV bits
    (other IV bits = 0), of the first output bit of R-round Trivium.
    """
    total = 0
    for a in range(2 ** len(cube)):
        iv = [0] * 80
        # TODO: set the cube bits of `iv` from the integer `a`:
        #       bit j of `a` goes to IV position cube[j]  (positions are 1-based!)
        # TODO: z = first output bit of Trivium(key_bits, iv, init_rounds=R)
        #       total ^= z
        raise NotImplementedError("cube_sum")
    return total

def is_constant(cube, R, n_keys=50):
    """True if cube_sum gives the same value for n_keys random keys.
    Stop EARLY as soon as two different values appear: a non-constant cube is
    usually detected after 2-3 keys, so only constant cubes cost all n_keys."""
    first = None
    for _ in range(n_keys):
        key = [random.getrandbits(1) for _ in range(80)]
        # TODO: v = cube_sum(key, cube, R)
        #       remember the first value; if a later v differs, return False
        raise NotImplementedError("is_constant")
    return True

def max_rounds(cube, start=100, screen_keys=10, confirm_keys=50):
    """Largest R for which the cube sum is still constant.
    Search upwards (steps of 10, then 1) with a cheap screen of `screen_keys`
    keys, then CONFIRM the answer with `confirm_keys` keys, stepping down if
    the confirmation fails."""
    R = start
    while is_constant(cube, R + 10, screen_keys):
        R += 10
    while is_constant(cube, R + 1, screen_keys):
        R += 1
    while R > 0 and not is_constant(cube, R, confirm_keys):
        R -= 1                      # the screen was too optimistic
    return R

if __name__ == '__main__':
    # B2: try some cubes.  Extend this list in your experiments.
    for cube in ([1], [1, 4], [1, 4, 7, 10], [1, 4, 7, 10, 13, 16]):
        print(f"cube {cube}: constant up to R = {max_rounds(cube)}")
