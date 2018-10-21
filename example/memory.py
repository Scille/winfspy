import winfspy


def main():
    import pdb; pdb.set_trace()
    winfspy.lib.FspServiceRunEx("passthrough", winfspy.lib.SvcStart, winfspy.lib.SvcStop, winfspy.ffi.NULL, winfspy.ffi.NULL)


if __name__ == '__main__':
    main()
