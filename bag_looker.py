from math import log
from eth_abi.packed import encode_abi_packed
from Crypto.Hash import keccak
from lists import *


prefixes = [b"RING", b'NECK', b'HAND', b'FOOT', b'WAIST', b'HEAD', b'CHEST', b'WEAPON'][::-1]
source_arrays = [weapons, chestArmor, headArmor, waistArmor, footArmor, handArmor, necklaces, rings]
colors = ["#838383", "#00DC82", "#f8b73e", "#ff44b7"]


def random(inp):
    return keccak256(encode_abi_packed(('bytes',), (inp,)))


def keccak256(inp):
    k = keccak.new(digest_bits=256)
    k.update(inp)
    return int('0x'+k.hexdigest(), 16)


def pluck(token_id, key_prefix, source_array):
    token_id = b'%d' % token_id
    tmp = encode_abi_packed(['bytes']*2, (key_prefix, token_id))
    rand = random(tmp)
    output = source_array[rand % len(source_array)]
    greatness = rand % 21
    level = 0
    if greatness < 15:
        probability = 15 / 21 * 1 / len(source_array)
    elif greatness > 14:
        output += ' ' + suffixes[rand % len(suffixes)]
        probability = 4/21 * 1/len(suffixes) * 1/len(source_array)
        level = 1
        if greatness >= 19:
            name = [None, None]
            name[0] = namePrefixes[rand % len(namePrefixes)]
            name[1] = nameSuffixes[rand % len(nameSuffixes)]
            if greatness == 19:
                output = f'"{name[0]} {name[1]}" {output}'
                level = 2
            else:
                output = f'"{name[0]} {name[1]}" {output} +1'
                level = 3
            probability = 1/21 * 1/len(namePrefixes) * 1/len(nameSuffixes) * 1/len(source_array) * 1/len(suffixes)
    return output, greatness, probability, level


def get_stats(token_id):
    stats = {'greatness': [], 'total': 0, 'items': [], 'colors': [],
             'probabilities': [], 'log_prob': 0}
    for key_prefix, source in zip(prefixes, source_arrays):
        output, greatness, probability, level = pluck(token_id, key_prefix, source)
        stats['greatness'].append(greatness)
        stats['total'] += greatness
        stats['items'].append(output)
        stats['colors'].append(colors[level])
        stats['probabilities'].append(probability)
        stats['log_prob'] += log(probability)
    return stats
