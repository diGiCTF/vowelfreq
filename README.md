# VowelFreq

This script analyzes a wordlist to identify and extract common letter patterns based on vowel and consonant placements. It processes words of specified lengths, detects recurring patterns, and generates an Excel file with detailed analysis, including vowel position statistics and matching word patterns.

## Features

- ✅ **Pattern Matching**: Identifies patterns in words based on vowels (`?1`) and non-vowels (`?2`).
- ✅ **Custom Word Length Ranges**: Allows specifying minimum and maximum word lengths to analyze.
- ✅ **Excel Report Generation**: Saves results in `pattern_results.xlsx`, with:
  - A **vowel position analysis** table.
  - Separate sheets for different word lengths with matching word statistics.
- ✅ **Threshold Filtering**: Excludes patterns with fewer than four matches or a match percentage ≤ 0.10%.
- ✅ **Efficient Processing**: Groups words by length to optimize pattern generation.
- ✅ **Bold Formatting in Excel**: Enhances readability of headers and first columns.
- ✅ **Command-Line Interface (CLI)**: Easy to run with simple arguments.

## Installation

Ensure you have Python installed, along with the required dependencies:

```bash
pip install pandas openpyxl
python vowelfreq.py --input dictionary_words_lower_350k.txt --min 6 --max 11
Processing words between 6 and 11 characters...

[INFO] Generating vowel position analysis...
[INFO] Processing words of length 6...
[INFO] Processing words of length 7...
...
✅ Processing complete! Results saved to pattern_results.xlsx
```

## Results
The resulting pattern_results.xlsx contains:

- Vowel Analysis (distribution of vowels in words)
- Sheets for different word lengths with:
- Pattern (e.g., ?1?2?1?2?2)
- Matching Words (count of words fitting the pattern)
- Percentage (match frequency in the dataset)
