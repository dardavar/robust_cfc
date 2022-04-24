from bitstring import BitArray
import numpy as np

M = 4


class ParallelTagEncoderM4T3:

    @staticmethod
    def create_cnt_iter(t, init, is_sl=False):
        pow_vec = [0]*t
        pow_vec[-1] = init
        sl_diff = 1 if is_sl else 0
        while True:
            prev_rst = False
            for idx in range(t):
                if pow_vec[idx] == pow_vec[-1] - sl_diff and idx != t-1:
                    pow_vec[idx] = 0
                    prev_rst = True
                elif prev_rst or idx == 0:
                    pow_vec[idx] += 1
                    if not is_sl and idx == t - 1:  # since the last bit inc by 2
                        pow_vec[idx] += 1
                    yield idx
                    break

    @staticmethod
    def compute_x_powers(x, bb_size, t, gf):
        odd_leq_cnt = ParallelTagEncoderM4T3.create_cnt_iter(t, 1)
        even_leq_cnt = ParallelTagEncoderM4T3.create_cnt_iter(t, 2)
        sl_cnt = ParallelTagEncoderM4T3.create_cnt_iter(t, 1, is_sl=True)
        x_regs = gf([
            [x[2], x[2], x[2]],
            np.power([x[2], x[2], x[2]], 2),
            [x[1], x[1], x[1]],
            [x[0], x[0], x[0]]])
        all_x_seq = x_regs[:, 0]
        for i in range(M, bb_size, M):
            odd_leq_inc = next(odd_leq_cnt)
            even_leq_inc = next(even_leq_cnt)
            sl_inc = next(sl_cnt)
            next_x_seq = [x_regs[0, odd_leq_inc] * x[odd_leq_inc],
                          x_regs[1, even_leq_inc] * x[even_leq_inc],
                          x_regs[2, sl_inc] * x[(sl_inc + 1) % 3],
                          x_regs[3, sl_inc] * x[(sl_inc + 2) % 3]]
            all_x_seq = np.append(all_x_seq, next_x_seq)
            ones_mat = gf.Ones((4, 3))
            ones_mat[0, :odd_leq_inc + 1] = next_x_seq[0]
            ones_mat[1, :even_leq_inc + 1] = next_x_seq[1]
            ones_mat[2, :sl_inc + 1] = next_x_seq[2]
            ones_mat[3, :sl_inc + 1] = next_x_seq[3]
            x_regs *= ones_mat
        return all_x_seq

    @staticmethod
    def convert_bb_to_gf_2_r(bb, r, gf):
        bin_arr = BitArray(hex=bb)
        bin_arr += BitArray(bin='0'*(r - (len(bin_arr) % r)))  # append with zero to a multiplication of r
        bb = gf([bin_arr[i:i+r].uint for i in range(0, len(bin_arr), r)])
        return np.append(bb, gf.Zeros(M - (len(bb) % M)))

    @staticmethod
    def compute_tag(bb, secret, gf, r, t):
        secret = gf(secret)
        if isinstance(bb, str):
            bb = ParallelTagEncoderM4T3.convert_bb_to_gf_2_r(bb, r, gf)
        else:
            bb = np.append(gf(bb), gf.Zeros(M - (len(bb) % M)))
        x_powers = ParallelTagEncoderM4T3.compute_x_powers(secret, len(bb), t, gf)
        return bb.dot(x_powers)
