# README - extraire.py

## Purpose

`extraire.py` is a Python script designed to extract medication names from HTML files in the VIDAL medical database. The script performs web scraping on local HTML files to extract pharmaceutical entities organized by active substance, and generates a DELAF format dictionary suitable for use with UNITEX natural language processing tools.

---

## Requirements

### Dependencies
- Python 3.x
- `os` module (built-in)
- `re` module (Regular expressions - built-in)
- `sys` module (built-in)
- `unicodedata` module (built-in)

### Input Files
- **VIDAL HTML Files** (folder containing multiple HTML files)
  - Encoding: UTF-8 without BOM
  - Format: HTML files with medication data
  - Naming convention: `vidal-Sommaires-Substances-X.htm` (where X is a letter A-Z)
  - Example files: `vidal-Sommaires-Substances-A.htm`, `vidal-Sommaires-Substances-B.htm`, etc.
  - Content: Contains medication names in `<a>` tags organized by first letter

### Server Setup (Optional - for local development)
- **Apache Web Server** (e.g., XAMPP) for serving HTML files locally
- HTTP port configuration (default: 80)
- **Note**: This version does not require HTTP parameters; it reads files directly from the filesystem

---

## Usage

### Basic Usage
```bash
python extraire.py <VIDAL_folder_path>
```

### Command-Line Arguments
- **Argument 1** (Required): Path to the VIDAL folder containing HTML files
  - Type: Directory path
  - Example: `python extraire.py C:\path\to\VIDAL`
  - Example: `python extraire.py ./VIDAL`

### Example Commands
```bash
# Windows
python extraire.py "C:\Users\YourName\Desktop\VIDAL"

# Linux/Mac
python extraire.py "/home/user/VIDAL"

# Relative path
python extraire.py ./VIDAL
```

### Error Handling
- **Missing argument**: Script will display usage instructions
- **Invalid folder path**: Script will report folder does not exist
- **No HTML files**: Script will process empty directory without crashing

---

## Output Files

### 1. **subst.dic** (DELAF Dictionary)
- **Encoding**: UTF-16 LE with BOM (UCS-2 LE BOM)
- **Format**: DELAF (UNITEX dictionary format)
- **Content**: All medication names extracted from VIDAL HTML files
- **Properties**:
  - One medication per line
  - Each entry format: `medication_name,.N+subst`
  - Sorted in processing order (not alphabetically sorted)
  - Contains all medications from all processed files
  - No duplicate removal (duplicates are kept as-is)

### 2. **infos1.txt** (Extraction Statistics)
- **Encoding**: UTF-8
- **Content**:
  - Number of medications extracted for each letter (A-Z)
  - Total count of all medications extracted
  - Format: Letter followed by entity count on each line
- **Example Output**:
  ```
  A : 245 entités
  B : 189 entités
  C : 312 entités
  ...
  Z : 45 entités
  Total : 5847 entités
  ```

---

## How It Works

### Step 1: Validate Input
- Checks if the correct number of command-line arguments is provided
- Verifies that the provided directory exists
- Exits with error message if validation fails

### Step 2: Initialize Variables
- Creates empty list to store medication names
- Prepares to scan the VIDAL directory

### Step 3: Process HTML Files
- Iterates through all files in the VIDAL directory
- Identifies HTML files (`.htm` or `.html` extensions)
- Extracts target letter from filename
  - Example: `vidal-Sommaires-Substances-A.htm` → target letter is 'A'
- Extracts the letter from the filename by finding the last hyphen-separated segment

### Step 4: Extract Medication Names
**Function**: `extraire_noms_medicaments()`
- Reads each HTML file with UTF-8 encoding
- Uses regex pattern to find all text within `<a>` tags: `<a[^>]*>([^<]+)</a>`
- Filters matches based on:
  - Starts with the target letter (case-insensitive)
  - Contains accented characters using Unicode normalization
  - Contains more than 1 character
  - Medication name in lowercase format
- Returns list of filtered medication names

### Step 5: Normalize Accents
**Function**: `normaliser_lettre()`
- Uses Unicode NFD normalization to handle French accented characters
- Removes accents for comparison purposes
- Allows matching of letters like 'Á' with 'A'
- Example: 'Élévé' → compares as 'Eleve' for first letter

### Step 6: Create Alphabetical Dictionary
**Function**: `creer_dictionnaire_alfabetique()`
- Organizes medications by their first letter
- Creates DELAF format entries: `medication_name,.N+subst`
- Returns dictionary with structure:
  ```python
  {
    'a': ['abacavir,.N+subst', 'abatacept,.N+subst', ...],
    'b': ['baclofen,.N+subst', ...],
    ...
  }
  ```

### Step 7: Generate DELAF Dictionary
**Function**: `generer_delf()`
- Opens output file with UTF-16 LE encoding
- Writes BOM character (`\ufeff`) at the beginning
- Writes each medication in DELAF format: `name,.N+subst\n`
- Closes the file properly

### Step 8: Generate Statistics
**Function**: `generer_infos()`
- Opens `infos1.txt` for writing (UTF-8 encoding)
- Iterates through alphabetical dictionary in sorted order
- Counts medications for each letter
- Calculates total count
- Writes statistics in human-readable format

### Step 9: Display Console Output
- Prints statistics for each letter to console
- Prints total count
- Displays completion message

---

## Function Reference

### `normaliser_lettre(lettre)`
Normalizes a letter to ignore accents using Unicode NFD decomposition.
- **Input**: Single letter (string)
- **Output**: Normalized letter without accents (string)
- **Example**: 'É' → 'E'

### `extraire_noms_medicaments(fichier_html, lettre_cible)`
Extracts medication names from an HTML file, filtered by target letter.
- **Input**: 
  - `fichier_html`: Path to HTML file (string)
  - `lettre_cible`: Target letter to filter by (string)
- **Output**: List of medication names (list)
- **Regex Pattern**: `<a[^>]*>([^<]+)</a>`

### `creer_dictionnaire_alfabetique(noms_medicaments)`
Creates an alphabetical dictionary of medications in DELAF format.
- **Input**: List of medication names (list)
- **Output**: Dictionary organized by first letter (dict)

### `generer_delf(noms_medicaments, fichier_sortie)`
Generates a DELAF format dictionary file.
- **Input**:
  - `noms_medicaments`: List of medications (list)
  - `fichier_sortie`: Output filename (string)
- **Output**: Writes to file (no return value)
- **Encoding**: UTF-16 LE with BOM

### `generer_infos(dictionnaire, fichier_infos)`
Generates statistics file with medication counts per letter.
- **Input**:
  - `dictionnaire`: Alphabetical dictionary (dict)
  - `fichier_infos`: Output filename (string)
- **Output**: Writes to file (no return value)
- **Encoding**: UTF-8

### `traiter_dossier_vidal(dossier_vidal)`
Main processing function that orchestrates the entire extraction workflow.
- **Input**: Path to VIDAL directory (string)
- **Output**: Generates `subst.dic` and `infos1.txt`

---

## Example Output

### subst.dic Sample
```
abacavir,.N+subst
abatacept,.N+subst
abciximab,.N+subst
abiratérone,.N+subst
abiraterone,.N+subst
acarbose,.N+subst
acebutolol,.N+subst
acetaminophen,.N+subst
...
```

### infos1.txt Sample
```
A : 245 entités
B : 189 entités
C : 312 entités
D : 267 entités
E : 198 entités
F : 145 entités
G : 132 entités
H : 98 entités
I : 156 entités
J : 87 entities
K : 54 entités
L : 203 entités
M : 289 entités
N : 167 entités
O : 76 entités
P : 234 entités
Q : 45 entités
R : 198 entités
S : 276 entités
T : 213 entités
U : 92 entités
V : 134 entités
W : 23 entités
X : 15 entités
Y : 8 entités
Z : 12 entités
Total : 4847 entités
```

### Console Output
```
A : 245 entités
B : 189 entités
C : 312 entités
...
Z : 12 entités
Total : 4847 entités
Extraction terminée. Fichiers 'subst.dic' et 'infos1.txt' générés.
```

---

## Key Features

✅ **Unicode Support**: Full support for French accented characters (é, è, ê, ç, etc.)
✅ **Accent Normalization**: Compares letters ignoring accents for proper filtering
✅ **DELAF Compliance**: Output format fully compatible with UNITEX dictionaries
✅ **Proper Encoding**: UTF-16 LE with BOM for dictionary files, UTF-8 for statistics
✅ **Error Handling**: Validates input directory and arguments
✅ **Console Feedback**: Real-time statistics display during processing
✅ **Flexible Input**: Works with any directory structure containing HTML files
✅ **Statistics Generation**: Comprehensive counts per letter and total

---

## Technical Notes

### Regular Expression Pattern
```regex
<a[^>]*>([^<]+)</a>
```
- Matches opening `<a>` tag with any attributes
- Captures all text content between tags (group 1)
- Non-greedy matching to avoid capturing closing tags
- Flag `re.S` allows dot to match newlines

### Unicode Normalization
- Uses NFD (Canonical Decomposition) form
- Converts combined characters to base + diacritics
- Allows ASCII encoding to remove diacritics
- Example: 'café' → 'cafe' for comparison

### File Encoding Handling
- Input HTML: UTF-8 (preserves original encoding as per requirements)
- Output Dictionary: UTF-16 LE with BOM (UNITEX standard)
- Output Statistics: UTF-8 (human-readable format)
- BOM written explicitly as `\ufeff` character

### Performance Considerations
- Single-pass file reading and processing
- Regex compilation within functions (not pre-compiled for clarity)
- List operations suitable for typical VIDAL dataset sizes
- No memory-intensive operations on large files

---

## Common Issues & Solutions

### Issue: "Erreur : le dossier ... n'existe pas"
**Solution**: Verify the VIDAL folder path is correct and the directory exists
```bash
# Check if directory exists (Windows)
dir "C:\path\to\VIDAL"

# Check if directory exists (Linux/Mac)
ls -la /path/to/VIDAL
```

### Issue: No medications extracted (empty subst.dic)
**Possible Causes**:
- HTML files not in expected format with `<a>` tags
- Medication names don't match the filtering criteria
- Files have different encoding than UTF-8

**Solution**: 
- Verify HTML file structure and content
- Check medication naming conventions
- Ensure files are UTF-8 encoded

### Issue: Special characters appear as garbage in output
**Solution**: Verify the output file is opened with UTF-16 LE encoding
- The script includes BOM character explicitly
- Use proper text editors that support UTF-16 LE

### Issue: Accented characters not recognized
**Solution**: Ensure input HTML files are UTF-8 encoded without BOM
- The normalization function should handle French accents (é, è, ê, ç)
- Test with individual files to isolate issues

### Issue: Script requires two arguments (interval + port) but here only needs one
**Note**: This version of the script only requires the VIDAL folder path. If integration with HTTP server is needed, modify to accept additional arguments for:
- HTTP port number (default: 80)
- Letter interval (e.g., A-Z, A-M, N-Z)

---

## Integration with Other Components

This script is **Step 1** of the medical information extraction project:
1. ✅ **extraire.py** (current) - Extracts base dictionary from VIDAL
2. **enrichir.py** - Enriches dictionary with corpus data
3. **unitex.py** - Applies extraction patterns using UNITEX
4. **sqlite.py** - Stores results in database

The output `subst.dic` from this script is the input for `enrichir.py` in the next phase.

---

## Author Notes

This extraction script forms the foundation of the medical information extraction system. The DELAF dictionary it generates (`subst.dic`) serves as the basis for advanced natural language processing tasks, particularly medication name recognition and posology extraction using UNITEX grammars.

The script's design emphasizes:
- **Reliability**: Proper error handling and validation
- **Standards Compliance**: DELAF format for UNITEX compatibility
- **Localization**: Full support for French medical terminology with accents
- **Maintainability**: Clear function separation and documentation
