def position_r_to_f(p_r, c_o):
    p_f = p_r + c_o
    return p_f


def calibrate_position(p_f, p_f_0, p_r_0, w, c_o):
    if p_f < p_f_0:  # reverse movement
        s_r = p_f_0 - p_f  # reverse steps
        c_term = w * s_r  # calibration term
        p_r = p_r_0 - s_r - c_term  # apply reverse steps and calibration
        c_o_updated = c_o + c_term  # update calibration offset
        return p_r, c_o_updated
    else:  # forward movement
        s_f = p_f - p_f_0  # forward steps
        p_r = p_r_0 + s_f  # apply forward steps
        return p_r, c_o
