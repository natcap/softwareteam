import argparse
import datetime
import itertools
import os
import sys


DATE_FMT = '%Y-%m-%d'  # YYYY-MM-DD


def main(args):
    """Determine next rotations for rotations.txt.

    Order of the printed text is determined by the latest 4 rotations in
    rotations.txt, and the dates printed will be in 1-week increments starting
    the week following the final week in rotations.txt.

    Args:
        args (list): A list of command-line parameters to parse.

    Returns:
        ``None``.
    """
    parser = argparse.ArgumentParser(
        description=(
            "Print the next rotations for rotations.txt to stdout. "
            "Order from the final 4 weeks of the file is retained, "
            "and the rotation dates start on the next chronological "
            "week. Recommended usage: "
            " $ python extend-rotations.py 10 >> rotations.txt "))
    parser.add_argument(
        'n_weeks', help="The number of weeks to append to rotations.txt.")

    parsed_args = parser.parse_args(args)

    last_date = None
    with open(os.path.join(os.path.dirname(__file__),
                           'rotations.txt')) as rotations_file:
        # Determine the order of team members based on the latest known
        # non-repeating names.  This extra (mild) complexity is helpful for
        # whenever we hire again.
        names = []  # In chronological order, pos. 0 is earliest.
        for line in reversed(rotations_file.read().strip().split('\n')):
            date, name = line.split(' ')

            if name in names:
                break

            if not last_date:
                last_date = datetime.datetime.strptime(
                    date, DATE_FMT).date()

            # Insert team_members in increasing chronological order of latest
            # known forums rotation assignment.
            names.insert(0, name)

    one_week = datetime.timedelta(days=7)
    for index, name in zip(
            range(int(parsed_args.n_weeks)),
            itertools.cycle(names)):
        last_date += one_week

        # Sanity check that this date is still a Monday (0th day of week)
        assert last_date.weekday() == 0

        print(f'{last_date.strftime(DATE_FMT)} {name}')


if __name__ == '__main__':
    main(sys.argv[1:])
