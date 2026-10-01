def rescale(x, a0, an, b0, bn):
    return b0 + (x - a0) * (bn - b0) / (an - a0)
