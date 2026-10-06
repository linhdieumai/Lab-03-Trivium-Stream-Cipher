"""
Track B, B3 --- a FAST cube sum (provided, you do not need to change it).

This computes exactly the same cube sums as your cube_sum in zero_sum.py, but
thousands of times faster, using "bit-slicing": a Python int is used as a
vector of lanes, each lane runs its own copy of Trivium, and one sequence of
big-integer XOR/AND operations clocks all lanes at once.

Use it ONLY after your own cube_sum works: first check that both agree on
small cubes (see check_fast.py), then use fast_is_constant for large cubes.
"""
import random

def _cube_masks(c, reps):
    """mask[j]: lanes whose t has bit j set, repeated for `reps` keys."""
    L = 1 << c
    # mask_j has bit t set iff (t >> j) & 1
    masks = []
    for j in range(c):
        m = 0
        period = 1 << (j + 1)
        unit = ((1 << (1 << j)) - 1) << (1 << j)          # bits [2^j, 2^(j+1)) set
        # replicate unit over L bits
        m = unit
        width = period
        while width < L:
            m |= m << width
            width <<= 1
        masks.append(m)
    full_seg = (1 << L) - 1
    rep = 0
    for i in range(reps):
        rep |= 1 << (i * L)
    return [m * rep for m in masks], full_seg * rep, rep

def cube_sums(cube, keys, rounds, fixed_iv=None, inner=None):
    """
    cube   : list of IV indices (1..80) that are summed over
    keys   : list of 80-bit keys (lists of bits K_1..K_80)
    rounds : sorted list of round numbers R; the superpoly of the first output
             bit of R-round Trivium is evaluated for every R in the list
    fixed_iv: dict {iv_index: bit} for non-cube IV bits (default all 0)
    inner  : number of cube variables handled inside the lanes (default: all,
             capped so that the lane width stays at most 2^22)
    returns: dict R -> list of superpoly values p_R(key), one per key
    """
    fixed_iv = fixed_iv or {}
    k, n = len(cube), len(keys)
    if inner is None:
        inner = k
        while inner > 0 and n * (1 << inner) > (1 << 22):
            inner -= 1
    c = inner
    L = 1 << c
    masks, FULL, rep = _cube_masks(c, n)
    # key words: lane block i gets key i
    key_words = []
    for b in range(80):
        w = 0
        for i, K in enumerate(keys):
            if K[b]:
                w |= ((1 << L) - 1) << (i * L)
        key_words.append(w)
    Rmax = rounds[-1]
    wanted = set(rounds)
    acc = {R: 0 for R in rounds}          # folded parity words (XOR over outer loop)
    outer = cube[c:]
    for a in range(1 << len(outer)):
        s = [0] * 289
        for b in range(80):
            s[1 + b] = key_words[b]
        for idx, bit in fixed_iv.items():
            s[93 + idx] = FULL if bit else 0
        for j, idx in enumerate(cube[:c]):
            s[93 + idx] = masks[j]
        for j, idx in enumerate(outer):
            s[93 + idx] = FULL if (a >> j) & 1 else 0
        s[286] = s[287] = s[288] = FULL
        for r in range(Rmax + 1):
            t1 = s[66] ^ s[93]; t2 = s[162] ^ s[177]; t3 = s[243] ^ s[288]
            if r in wanted:
                acc[r] ^= t1 ^ t2 ^ t3
            t1 ^= (s[91] & s[92]) ^ s[171]
            t2 ^= (s[175] & s[176]) ^ s[264]
            t3 ^= (s[286] & s[287]) ^ s[69]
            s[2:94] = s[1:93]; s[1] = t3
            s[95:178] = s[94:177]; s[94] = t1
            s[179:289] = s[178:288]; s[178] = t2
    # parity of every L-lane segment
    out = {}
    for R, z in acc.items():
        h = L >> 1
        while h:
            z ^= z >> h
            h >>= 1
        out[R] = [(z >> (i * L)) & 1 for i in range(n)]
    return out


def fast_cube_sum(key_bits, cube, R):
    """Same result as zero_sum.cube_sum(key_bits, cube, R)."""
    return cube_sums(cube, [key_bits], [R])[R][0]

def fast_is_constant(cube, R, n_keys=50, rng=None):
    """Same meaning as zero_sum.is_constant, evaluated for all keys in one run."""
    rng = rng or random.Random()
    keys = [[rng.getrandbits(1) for _ in range(80)] for _ in range(n_keys)]
    v = cube_sums(cube, keys, [R])[R]
    return all(x == v[0] for x in v)

def fast_max_rounds(cube, start=100, screen_keys=10, confirm_keys=50):
    """Same search as zero_sum.max_rounds, using the fast cube sum."""
    R = start
    while fast_is_constant(cube, R + 10, screen_keys):
        R += 10
    while fast_is_constant(cube, R + 1, screen_keys):
        R += 1
    while R > 0 and not fast_is_constant(cube, R, confirm_keys):
        R -= 1
    return R
