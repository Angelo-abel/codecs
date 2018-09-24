def progress(count, total, label)->None:
    bar_len: int = 60
    filled_len = int(round(bar_len * count / float(total)))
    percents: float = round(100.0 * count / float(total), 1)
    x: str = " "*int(filled_len)
    print("\x1b[2K \33[44m{}\33[0m {} \33[1;94m {}% {} \33[1;0m".format(x, str(" "*(bar_len-filled_len)), str(percents), label), end = '\r', flush = True)
