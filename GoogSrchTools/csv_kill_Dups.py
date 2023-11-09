"""
Refine news articles csv file: kill duplicates, handle line-breaks.
"""
import csv


def csv_kill_dups(read_file, write_file, key_unique):
    """
    Rewrite csv file killing duplicated values of 'key_unique'
    :param read_file:  path to input csv file - str
    :param write_file:   path to output csv file - str
    :param key_unique:  key of the values that to be unique - str
    """
    with (open(read_file) as in_file,
          open(write_file, "w", newline='') as out_file):
        unique = []
        fieldnames = csv.DictReader(in_file).fieldnames
        csv.DictWriter(out_file, fieldnames=fieldnames).writeheader()
        data = csv.DictReader(in_file, fieldnames=fieldnames)
        for i, row in enumerate(data):
            text = row[key_unique]  # The 'text' field to have unique values
            if text in unique:
                continue
            unique.append(text)
            refined_row = {}
            for k, v in row.items():
                # Remove unneeded newlines
                refined_row[k] = v.replace('\n', '')
            # Write the unique-text-value row in the out_file
            csv.DictWriter(out_file, fieldnames=fieldnames).writerow(refined_row)
        # print("unique:\n", unique)


if __name__ == '__main__':
    csv_kill_dups(
        read_file='../Kraken/re_csv/articles_data.csv',
        write_file='../Kraken/re_csv/articles_data_noDups.csv',
        key_unique='text')
