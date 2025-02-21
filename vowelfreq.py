import argparse
import itertools
import collections
import string
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font

# Define vowels and non-vowels sets
vowels = set("aeiouAEIOU")
non_vowels = set("bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ0123456789")

# Function to check if a word matches a given pattern
def matches_pattern(word, pattern):
    if len(word) != len(pattern) // 2:
        return False
    word = word.lower()
    pattern_tokens = [pattern[i:i+2] for i in range(0, len(pattern), 2)]

    for i, token in enumerate(pattern_tokens):
        if token == "?1" and word[i] not in vowels:
            return False
        elif token == "?2" and word[i] not in non_vowels:
            return False
    return True

# Function to generate patterns for a given word length
def generate_patterns(word_length):
    base_pattern = ["?2"] * word_length
    unique_patterns = set()

    for num_vowels in range(1, word_length - 1 + 1):
        for vowel_positions in itertools.combinations(range(word_length), num_vowels):
            pattern = base_pattern[:]
            for pos in vowel_positions:
                pattern[pos] = "?1"
            unique_patterns.add("".join(pattern))

    return sorted(unique_patterns)

# Function to process words and match patterns
def process_patterns(wordlist, patterns):
    total_words = len(wordlist)
    results = []

    for pattern in patterns:
        count_matching = sum(1 for word in wordlist if matches_pattern(word, pattern))
        percentage = (count_matching / total_words) * 100 if total_words > 0 else 0

        # Exclude patterns with 3 or fewer matches and percentage <= 0.10
        if count_matching > 3 and percentage > 0.10:
            results.append([pattern, count_matching, percentage])

    results.sort(key=lambda x: x[2], reverse=True)
    return results

# Function to analyze vowel positions and generate statistics
def analyze_vowel_positions(input_file):
    vowels_set = {'a', 'e', 'i', 'o', 'u'}
    vowel_counts = collections.defaultdict(lambda: collections.defaultdict(int))
    total_counts = collections.defaultdict(int)

    with open(input_file, 'r', encoding='utf-8') as file:
        for line in file:
            word = line.strip().lower()
            if not word or any(char not in string.ascii_lowercase for char in word):
                continue

            length = len(word)
            total_counts[length] += 1

            for i, char in enumerate(word):
                if char in vowels_set:
                    vowel_counts[length][i] += 1

    max_length = max(total_counts.keys(), default=0)
    data = {"Position": list(range(1, max_length + 1))}

    for length in sorted(total_counts.keys()):
        column_name = f"{length} length ({format(total_counts[length], ',')})"  # Format with commas
        percentages = [
            (vowel_counts[length][i] / total_counts[length]) * 100 if total_counts[length] > 0 else None
            for i in range(max_length)
        ]

        data[column_name] = percentages

    return pd.DataFrame(data)

# Command-line argument parsing
parser = argparse.ArgumentParser(description="Pattern matcher for wordlists")
parser.add_argument('--input', required=True, help='Specify the input file')
parser.add_argument('--min', type=int, required=True, help='Minimum word length (e.g., 6)')
parser.add_argument('--max', type=int, required=True, help='Maximum word length (e.g., 11)')
args = parser.parse_args()

if args.min > args.max:
    print("\nError: --min value cannot be greater than --max.\n")
    exit(1)
if args.min < 1:
    print("\nError: --min must be at least 1.\n")
    exit(1)

print(f"\nProcessing words between {args.min} and {args.max} characters...\n")

# Read words and group by length
word_groups = collections.defaultdict(list)
with open(args.input, "r") as f:
    for line in f:
        word = line.strip()
        if word and args.min <= len(word) <= args.max:
            word_groups[len(word)].append(word)

word_lengths = sorted(word_groups.keys())

# Create an Excel workbook
xlsx_filename = "pattern_results.xlsx"
wb = Workbook()

# First tab: Vowel Position Analysis with bold headers and first column
print("[INFO] Generating vowel position analysis...")
vowel_df = analyze_vowel_positions(args.input)
ws = wb.active
ws.title = "Vowel Analysis"
ws.append(vowel_df.columns.tolist())

# Apply bold formatting for headers and first column
for cell in ws[1]:
    cell.font = Font(bold=True)
for row in ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=1, max_col=1):
    for cell in row:
        cell.font = Font(bold=True)

# Write data row by row to Excel
for row in vowel_df.itertuples(index=False):
    ws.append([None if v is None else v for v in row])  # Ensure empty values are recognized

# Process each word length separately with bold headers
for i, word_length in enumerate(word_lengths):
    print(f"\n[INFO] Processing words of length {word_length}...")

    word_list = word_groups[word_length]
    patterns = generate_patterns(word_length)
    results = process_patterns(word_list, patterns)

    if not results:
        print(f"[INFO] Skipping length {word_length}, no patterns meeting threshold.")
        continue

    # Create a new sheet for this word length
    sheet_name = f"Length_{word_length}"
    ws = wb.create_sheet(title=sheet_name)
    ws.append(["Pattern", "Matching Words", "Percentage"])

    # Apply bold formatting to the first row (headers)
    for cell in ws[1]:
        cell.font = Font(bold=True)

    for row in results:
        ws.append(row)

    print(f"[INFO] Finished processing length {word_length}. {len(results)} patterns saved.")

# Save the Excel file
wb.save(xlsx_filename)
print(f"\n✅ Processing complete! Results saved to {xlsx_filename}\n")
