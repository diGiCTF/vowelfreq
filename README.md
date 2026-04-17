# vowelfreq.py

Standalone vowel-frequency pattern analyzer for any plaintext wordlist. Produces an Excel workbook in the same format used on [vowelfreq.com](https://vowelfreq.com), plus a sibling CSV for offline use.

Built for password-cracking research — the generated patterns use Hashcat custom-charset notation (`?1` for vowels, `?2` for non-vowels) so they can be dropped straight into a mask attack.

## What it does

Given a wordlist (one word per line), the script:

1. Filters to alpha-only words within your chosen length range.
2. Counts vowels per word and groups results by word length.
3. Extracts the observed vowel/non-vowel pattern for every word and tallies how often each pattern appears.
4. Writes the results to an xlsx workbook and a CSV.

## Requirements

- Python 3.8+
- `openpyxl`

```bash
pip install openpyxl
```

## Usage

```bash
python3 vowelfreq.py --input words.txt
```

### Options

| Flag | Default | Description |
|------|---------|-------------|
| `--input` | *(required)* | Path to a plaintext wordlist (one word per line). |
| `--min` | `3` | Minimum word length to include. |
| `--max` | `20` | Maximum word length to include. |
| `--output` | `pattern_results.xlsx` | Output xlsx path. |

### Examples

Analyze all words from length 3 through 20 (defaults):

```bash
python3 vowelfreq.py --input words.txt
```

Analyze only 6–9 character words:

```bash
python3 vowelfreq.py --input words.txt --min 6 --max 9
```

Run against `rockyou.txt` with a custom output path:

```bash
python3 vowelfreq.py --input rockyou.txt --min 4 --max 16 --output rockyou_patterns.xlsx
```

## Output

The script writes two files next to each other:

### 1. `pattern_results.xlsx`

**Sheet "Vowel Analysis"** — vowel-count distribution across all selected lengths:

| Word Length | 3 characters | 4 characters | 5 characters | ... |
|-------------|--------------|--------------|--------------|-----|
| Total Words | 1,234 | 5,678 | 9,012 | ... |
| 0 | 4.12 | 2.84 | 1.55 | ... |
| 1 | 48.71 | 35.02 | 22.14 | ... |
| 2 | 47.17 | 52.88 | 48.63 | ... |
| ... | ... | ... | ... | ... |

Column values are the percentage of words at that length with that many vowels.

**Sheets "Length_3", "Length_4", ...** — one sheet per word length containing the top patterns sorted by count descending:

| Pattern | Count | Percentage |
|---------|-------|-----------|
| `?2?1?2?1?2?1?2` | 412 | 18.34 |
| `?1?2?1?2?1?2?1` | 287 | 12.77 |
| ... | ... | ... |

### 2. `<stem>_vowel_counts.csv`

Flat CSV of the same vowel-count data, easy to grep / pipe:

```
Word Length,Vowel Count,Count,Total Words,Percentage
3,0,51,1234,4.12%
3,1,601,1234,48.71%
3,2,582,1234,47.17%
...
```

## How the pattern notation works

Every word is converted into a 2-character-per-letter mask:

- `?1` → vowel (`a`, `e`, `i`, `o`, `u`)
- `?2` → non-vowel (everything else)

So `password` becomes `?2?1?2?2?1?2?1?2` — and that's a hashcat mask you can run directly with your own `?1` / `?2` charset definitions:

```bash
hashcat -a 3 -m 0 hashes.txt -1 aeiou -2 bcdfghjklmnpqrstvwxyz ?2?1?2?2?1?2?1?2
```

## Why this is useful

Plain brute force with `?a` (full 95-char keyspace) scales terribly — `?a × 13` is `5.13 × 10²⁵` candidates, infeasible on a single GPU.

But real passwords are not random. They follow vowel/non-vowel patterns because humans pronounce words. Using the statistical distribution from a representative wordlist (like `rockyou.txt`), you can target the highest-probability masks first and crack realistic 13-character passwords in minutes instead of billions of years.

Run this script against your favorite wordlist, sort the per-length sheets by count, and feed the top N patterns into hashcat.

## License

MIT
