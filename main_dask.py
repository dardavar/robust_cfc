from tqdm import tqdm
import dask.dataframe as pd
import galois

# import utilities as utils
# from parallel_tag_encoder import ParallelTagEncoderM4T3
from error_applier import apply_error

MAX_BYTES_IN_BLOCK = 136
NUM_OF_ERRS_PER_SIZE = 1e6
if __name__ == '__main__':
    t = 3
    r = 8

    gf = galois.GF(2**r)
    tqdm.pandas()

    """
    Compute tha tag and write the DF to csv
    """
    # all_bbs_df = pd.read_csv(r'C:\Users\User\PycharmProjects\robust_cfc\unique_blocks.csv').dropna()
    # all_bbs_df = all_bbs_df.rename(columns={"BB": "bb_hex", "#": "num_of_bbs"})
    # all_bbs_df['size'] = all_bbs_df.apply(lambda row: int(len(row['bb_hex']) / 2), axis=1)
    # all_bbs_df['random_vector'] = utils.generate_random_vector((len(all_bbs_df), t), gf)
    # all_bbs_df['tag'] = all_bbs_df\
    #     .progress_apply(lambda row: ParallelTagEncoderM4T3.compute_tag(row['bb_hex'], row['random_vector'], gf, r, t),
    #                     axis=1)
    # all_bbs_df.to_csv(r'C:\Users\User\PycharmProjects\robust_cfc\unique_blocks.csv')
    all_bbs_df = pd.read_csv(r'C:\Users\User\PycharmProjects\robust_cfc\unique_blocks.csv', header=0).dropna()
    num_of_errors_to_apply = all_bbs_df['size'].value_counts().apply(lambda x: int(NUM_OF_ERRS_PER_SIZE/x))\
        .compute().to_dict()
    all_bbs_df['num_of_errs_to_apply'] = \
        all_bbs_df.apply(lambda row: num_of_errors_to_apply[row['size']], axis=1, meta=(None, 'int64'))
    all_bbs_df['rand_err_same_size_err_in_sig'] = \
        all_bbs_df.apply(lambda row:
                         apply_error(row, 10, row['num_of_errs_to_apply'], all_bbs_df, gf, r, t,
                                     random_err=True,
                                     err_in_sig=True), axis=1)
    all_bbs_df.to_csv(r'C:\Users\User\PycharmProjects\robust_cfc\unique_blocks.csv')





