import os
from argparse import ArgumentParser

import pdf2image


def main(args):
    converted = pdf2image.convert_from_path(args.i, dpi=300)
    cnt = 0
    first_part = os.path.join(args.o)
    for page in converted:
        page.save(os.path.join(first_part, str(cnt) + '.jpg'), 'JPEG')
        cnt += 1


if __name__ == '__main__':
    parser = ArgumentParser(add_help=True)
    parser.add_argument('-i', type=str, help='Path to pdf doc')
    parser.add_argument('-o', default='1065dataset/images',
                        help='Path to output folder')
    args_ = parser.parse_args()
    main(args_)
