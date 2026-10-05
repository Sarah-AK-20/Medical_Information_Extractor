# README - enrichir.py

## Purpose

`enrichir.py` is a Python script designed to enrich and update a medical dictionary (DELAF format) with new medication names extracted from a medical corpus. The script reads an existing dictionary (`subst.dic`) and augments it with additional medication entities found in a medical text corpus.

---

## Requirements

### Dependencies
- Python 3.x
- `re` module (Regular expressions - built-in)
- `os` module (built-in)
- `sys` module (built-in)

### Input Files
1. **`subst.dic`** - Existing dictionary of medication names by active substance
   - Encoding: UTF-16 LE with BOM
   - Format: DELAF (UNITEX dictionary format)
   - Each entry format: `medicament_name,.N+subst`

2. **`corpus-medical.txt`** (or custom path)
   - Encoding: UTF-8 without BOM
   - Contains medical prescriptions and medication information
   - Default path: `corpus-medical.txt` (can be provided as command-line argument)

---

## Usage

### Basic Usage
```bash
python enrichir.py
```
Uses the default corpus file: `corpus-medical.txt`

### With Custom Corpus File
```bash
python enrichir.py path/to/corpus-medical.txt
```

### Command-Line Arguments
- **Argument 1** (Optional): Path to the medical corpus file
  - Default: `corpus-medical.txt`
  - Example: `python enrichir.py my_corpus.txt`

---

## Output Files

### 1. **subst.dic** (Enriched Dictionary)
- **Encoding**: UTF-16 LE with BOM (preserved from original)
- **Format**: DELAF dictionary format
- **Content**: All medications from original `subst.dic` + new medications from corpus
- **Properties**:
  - No duplicates
  - Sorted alphabetically (a-z)
  - Each entry: `medication_name,.N+subst`

### 2. **subst_corpus.dic** (Corpus Medications Dictionary)
- **Encoding**: UTF-16 LE with BOM
- **Format**: DELAF dictionary format
- **Content**: Only medications extracted from the medical corpus
- **Properties**:
  - No sorting applied
  - No duplicate removal
  - All entries in lowercase
  - Each entry: `medication_name,.N+subst`

### 3. **infos2.txt** (Corpus Statistics)
- **Encoding**: UTF-8
- **Content**: 
  - Number of medications from corpus for each letter (a-z)
  - Total count of medications from corpus
  - Format: Grouped by alphabetical letter with separators

### 4. **infos3.txt** (Enrichment Statistics)
- **Encoding**: UTF-8
- **Content**: 
  - Number of new medications added for each letter (a-z)
  - Total count of new medications added to dictionary
  - Format: Grouped by alphabetical letter with separators

---

## How It Works

### Step 1: Read Input Files
- Opens existing `subst.dic` dictionary (UTF-16 LE)
- Removes BOM character and parses entries
- Creates a set of existing medications (without DELAF tags)
- Reads medical corpus file (UTF-8)
- Replaces non-breaking spaces with regular spaces

### Step 2: Pattern Matching
Uses a regular expression pattern to extract medication names with dosage information:
```regex
^[ 0-9\tØ-]*([A-Za-zéèê]{3,})( LP)?[ :]*?(\d+(\.\d+|,\d+)?|(un|deux|trois|quatre|cinq|six|sept|huit|neuf|dix)[ ])[ :]*?(mg|U[ ]|UI|g|µg|ml|[,: ]?[ ]?\d*?(/j|sachet(s)?))
```

**Pattern Details**:
- Matches medication names (3+ characters, including accented characters)
- Captures dosage amounts (numeric or word-based: un, deux, trois, etc.)
- Matches various dosage units (mg, UI, g, µg, ml, etc.)
- Case-insensitive matching

### Step 3: Create Corpus Dictionary
- Extracts all medications from corpus using regex pattern
- Converts all entries to lowercase
- Writes to `subst_corpus.dic` (UTF-16 LE with BOM)
- Stores in memory for further processing

### Step 4: Enrich Dictionary
- Merges existing medications with new corpus medications using set union
- Identifies enrichment subset (new medications only)
- Removes duplicates automatically (using set operations)
- Sorts all medications alphabetically
- Writes enriched dictionary to `subst.dic` (UTF-16 LE with BOM)

### Step 5: Generate Statistics Files
- **infos2.txt**: Counts medications from corpus grouped by first letter
- **infos3.txt**: Counts new medications added (enrichment only) grouped by first letter
- Both files include letter-by-letter breakdown and totals

---

## Example Output Format

### subst.dic (enriched)
```
abacavir,.N+subst
abatacept,.N+subst
abciximab,.N+subst
abiratérone,.N+subst
acetaminophene,.N+subst
...
```

### infos2.txt
```
------------------------------------------
Total de A = 15
------------------------------------------
amoxicilline
ampicilline
...
------------------------------------------
Total de B = 8
------------------------------------------
...
Nombre total des substances actives = 250
```

### infos3.txt
```
------------------------------------------
Total de A = 3
------------------------------------------
amiodarone
atenolol
...
```

---

## Key Features

✅ **Duplicate Removal**: Set operations ensure no duplicate entries
✅ **Case Normalization**: All entries converted to lowercase
✅ **Encoding Preservation**: Original encoding formats maintained
✅ **Flexible Input**: Default or custom corpus file path
✅ **Comprehensive Statistics**: Letter-by-letter and total counts
✅ **Pattern Matching**: Regex extraction of medication names with dosages
✅ **Alphabetical Sorting**: Output dictionary sorted a-z

---

## Technical Notes

- **Set Operations**: Used for fast duplicate detection and removal
- **Regular Expressions**: Pattern designed to match French medication names with dosage information
- **Encoding**: Careful handling of UTF-16 LE BOM for DELAF format compliance
- **Memory Efficient**: Uses sets and generators where possible
- **Case Insensitivity**: Regex flags `re.I` and `re.M` for multiline case-insensitive matching

---

## Common Issues

### Issue: BOM character appears in output
**Solution**: The script explicitly removes BOM from input and adds it back using `\ufeff` marker

### Issue: Medications not found in corpus
**Solution**: Ensure medication names are 3+ characters and include dosage information matching the regex pattern

### Issue: File encoding errors
**Solution**: Verify input files have correct encoding:
- `subst.dic`: UTF-16 LE with BOM
- `corpus-medical.txt`: UTF-8 without BOM

---

## Author Notes

This script is part of a medical information extraction project (Étape 2) that enriches DELAF dictionaries with corpus-extracted medication data for use in UNITEX natural language processing.
