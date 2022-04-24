import numpy as np
import utilities as utils
from parallel_tag_encoder import ParallelTagEncoderM4T3


def random_error_in_vectors(gf, num_of_vecs, vec_len):
    return utils.generate_random_vector((num_of_vecs, vec_len), gf)


def replace_bb(df, new_bb_size, num_of_bbs):
    df = df[df['size'] == new_bb_size]
    return df.sample(min(num_of_bbs, len(df)))['bb_hex']


def compare_tags(off_tag, on_tag):
    return off_tag == on_tag


def apply_error(row, num_of_errs, new_bb_size, df, gf, r, t, random_err=True, err_in_sig=True):
    off_tag = gf(row['tag'])
    secret = row['random_vector']
    err_blocks = random_error_in_vectors(gf, num_of_errs, new_bb_size) if random_err \
        else replace_bb(df, new_bb_size, num_of_errs)
    res = []
    for err_bb in err_blocks:
        if err_in_sig:
            off_tag = random_error_in_vectors(gf, 1, 1)[0][0]
            secret = random_error_in_vectors(gf, 1, t)[0]
        on_tag = ParallelTagEncoderM4T3.compute_tag(err_bb, secret, gf, r, t)
        res.append(compare_tags(off_tag, on_tag))
    return np.count_nonzero(res)
