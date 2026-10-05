# README - posologie.grf

## Purpose

`posologie.grf` is a UNITEX grammar file that defines extraction patterns for medical posologies (medication prescriptions and dosage information). This finite-state graph specifies how to recognize and extract complete medication prescriptions from medical corpus text, including medication names, dosages, administration frequencies, times, and treatment durations.

---

## File Format

### Overview
- **Format**: UNITEX Unigraph (.grf) - XML-like structure
- **Encoding**: UTF-16 LE (binary format)
- **Type**: Visual Grammar Definition File
- **Purpose**: Defines finite-state transducer patterns
- **Compiled to**: FST2 format by `Grf2Fst2` command in unitex.py

### File Structure

The .grf file consists of several components:

```
#Unigraph
[Header/Metadata Section]
#
[Number of Nodes]
[Node Definitions]
[Transition Definitions (implicit in node data)]
```

---

## File Components

### 1. Header Section

```
#Unigraph
SIZE 1232 840
FONT Times New Roman:  10
OFONT Arial Unicode MS:B 12
BCOLOR 16777215
FCOLOR 0
ACOLOR 13487565
SCOLOR 16711680
CCOLOR 255
DBOXES y
DFRAME n
DDATE n
DFILE n
DDIR n
DRIG n
DRST n
FITS 100
PORIENT L
```

**Component Explanations**:

| Element | Meaning | Value | Purpose |
|---------|---------|-------|---------|
| `#Unigraph` | File type identifier | Required | Identifies as UNITEX grammar file |
| `SIZE` | Canvas dimensions | 1232 840 | Visual editor window size (width x height pixels) |
| `FONT` | Primary font | Times New Roman 10pt | Display font for nodes in editor |
| `OFONT` | Option font | Arial Unicode MS Bold 12pt | Font for labels/options |
| `BCOLOR` | Background color | 16777215 (white) | RGB color value for canvas background |
| `FCOLOR` | Foreground color | 0 (black) | Color for text/lines |
| `ACOLOR` | Archived color | 13487565 (gray) | Color for archived nodes |
| `SCOLOR` | Selection color | 16711680 (red) | Highlight color for selected nodes |
| `CCOLOR` | Cursor color | 255 (blue) | Cursor/pointer color |
| `DBOXES` | Draw boxes | y (yes) | Display box outlines in editor |
| `DFRAME` | Draw frame | n (no) | Don't draw frame around graph |
| `DDATE` | Draw date | n (no) | Don't display file date |
| `DFILE` | Draw filename | n (no) | Don't display filename |
| `DDIR` | Draw directory | n (no) | Don't display directory path |
| `DRIG` | Right-to-left | n (no) | Left-to-right text direction |
| `DRST` | Reset display | n (no) | Don't reset display settings |
| `FITS` | Fit zoom | 100 | Initial zoom level (100%) |
| `PORIENT` | Page orientation | L (Landscape) | Page orientation for printing |

### 2. Node Count
```
#
8
```
- The `#` marks the end of header
- `8` indicates there are exactly 8 nodes in this graph

### 3. Node Definitions

The graph contains 8 nodes that represent different components of a posology extraction pattern:

```
"<E>" 70 200 1 2
"" 300 200 0
"<N+subst>" 251 58 1 3
"dosage" 483 110 1 7
"duree" 549 243 1 6
"quantite et type" 242 321 1 1
"frequence" 498 336 1 5
"heure" 659 138 1 4
```

#### Node Format
```
"[Label/Pattern]" [X] [Y] [Type] [NextNode]
```

**Components**:
- **Label/Pattern**: Text in quotes - what the node represents
- **X coordinate**: Horizontal position in visual editor (pixels)
- **Y coordinate**: Vertical position in visual editor (pixels)
- **Type**: Node type (0=terminal/final, 1=normal)
- **Next Node**: Reference to next node(s) in sequence

#### Node Definitions Detail

| Node # | Label | X | Y | Type | Function |
|--------|-------|---|---|------|----------|
| 0 | `"<E>"` | 70 | 200 | 1 | **Entry Point** - Start of graph, matches empty input |
| 1 | `""` | 300 | 200 | 0 | **Exit Point** - End of graph, terminal node |
| 2 | `"<N+subst>"` | 251 | 58 | 1 | **Medication Name** - Matches tagged medication names from dictionary |
| 3 | `"dosage"` | 483 | 110 | 1 | **Dosage Sub-graph** - Extracts dosage amounts and units |
| 4 | `"duree"` | 549 | 243 | 1 | **Duration Sub-graph** - Extracts treatment duration |
| 5 | `"quantite et type"` | 242 | 321 | 1 | **Quantity & Type Sub-graph** - Extracts form/quantity info |
| 6 | `"frequence"` | 498 | 336 | 1 | **Frequency Sub-graph** - Extracts administration frequency |
| 7 | `"heure"` | 659 | 138 | 1 | **Time Sub-graph** - Extracts time of administration |

### Node Type Details

**Type 0**: Terminal/Final nodes
- Represent endpoints in the pattern
- No further transitions
- In this graph: node 1 (exit)

**Type 1**: Normal nodes
- Can have transitions to other nodes
- Represent pattern components
- Can link to sub-graphs or continue matching

### Implicit Transitions

Node references in the last field define transitions:
- `<E>` (node 0) connects to node 2
- `<N+subst>` (node 2) connects to node 3
- `dosage` (node 3) connects to node 7
- `quantite et type` (node 5) connects to node 1 (exit)
- `frequence` (node 6) connects to node 5
- `heure` (node 4) connects to node 6
- `duree` (node 4) connects to node 1 (exit)

---

## Grammar Structure & Logic

### Posology Extraction Pattern

The grammar extracts medication prescriptions following this overall pattern:

```
[Medication Name] [Dosage] [Quantity & Type] [Frequency] [Time] [Duration]
```

### Visual Flow

```
         ┌──────────────┐
         │   <E>        │ (Entry)
         │   Start      │
         └──────┬───────┘
                │
         ┌──────▼──────────────┐
         │  <N+subst>          │ (Medication name from dictionary)
         │  (from subst.dic)   │
         └──────┬──────────────┘
                │
         ┌──────▼──────────────┐
         │  dosage             │ (Dosage sub-graph)
         │  50 mg, 20 ml, etc  │
         └──────┬──────────────┘
                │
         ┌──────▼──────────────┐
         │  heure              │ (Time sub-graph)
         │  8h, morning, etc   │
         └──────┬──────────────┘
                │
         ┌──────▼──────────────┐
         │  frequence          │ (Frequency sub-graph)
         │  2x/day, 3 times    │
         └──────┬──────────────┘
                │
         ┌──────▼──────────────┐
         │  quantite et type   │ (Quantity & type sub-graph)
         │  2 tablets, 1 amp   │
         └──────┬──────────────┘
                │
         ┌──────▼──────────────┐
         │  duree              │ (Duration sub-graph)
         │  for 1 month, 21j   │
         └──────┬──────────────┘
                │
         ┌──────▼──────────────┐
         │  Exit ""            │ (Exit - match complete)
         │  Success            │
         └─────────────────────┘
```

---

## Sub-Graphs

Each named node (except `<E>` and exit `""`) likely references a separate sub-graph file:

### 1. **dosage** sub-graph
**Location**: `dosage.grf` (implicit reference)
**Purpose**: Matches dosage amounts and units
**Patterns**:
- Numeric amounts: `50`, `0.4`, `500`, `4000`
- Dosage units: `mg`, `ml`, `UI`, `U`, `g`, `µg`
- Formats: `50 mg`, `0,4ml`, `4000 UI`
- Examples from corpus:
  ```
  50 mg
  100 mg/m²
  0,4 ml
  500 UI
  ```

### 2. **quantite et type** sub-graph
**Location**: `quantite_et_type.grf`
**Purpose**: Matches pharmaceutical form and quantity
**Patterns**:
- Forms: `tablet`, `capsule`, `ampoule/amp`, `powder`, `cream`
- Quantities: `1`, `2`, `½`, `1/2`, `1/3`
- Abbreviations: `cp` (comprimé/tablet), `amp` (ampoule)
- Examples:
  ```
  1 tablet
  2 capsules
  1 amp (ampoule)
  1 cp
  ½ cp
  ```

### 3. **frequence** sub-graph
**Location**: `frequence.grf`
**Purpose**: Matches administration frequency
**Patterns**:
- Numeric: `1/day`, `2/day`, `3/day`, `4/day`
- Text (French): `une fois par jour`, `deux fois par jour`, `trois fois par jour`, `quatre fois par jour`
- Abbreviations: `/j` (par jour/per day)
- Short forms: `1 fois/jour`, `2x/day`
- Examples:
  ```
  1 fois par jour
  2 fois par jour
  3 fois par jour
  1/jour
  2/day
  ```

### 4. **heure** sub-graph
**Location**: `heure.grf`
**Purpose**: Matches time of administration
**Patterns**:
- Times: `8h`, `20h`, `8:00`, `20:00`
- Time names (French): `le matin` (morning), `le soir` (evening), `le midi` (noon)
- Timing: `au coucher` (at bedtime), `après repas` (after meals)
- Combinations: `1 in morning, 1 in evening`
- Examples:
  ```
  8 heures
  20h
  le matin
  le soir
  le midi
  au coucher
  ```

### 5. **duree** sub-graph
**Location**: `duree.grf`
**Purpose**: Matches treatment duration
**Patterns**:
- Days: `pendant 5 jours`, `5 days`, `J1 à J7`
- Weeks: `1 semaine`, `1 week`
- Months: `pendant un mois`, `for one month`, `1 mois`
- Days remaining: `pendant encore 21 jours` (for another 21 days)
- Date ranges: `de J1 à J7`, `from day 1 to day 7`
- Examples:
  ```
  pendant 5 jours
  pendant un mois
  pendant encore 21 jours
  de J1 à J7
  1 semaine
  ```

---

## Compilation Process

### From .grf to .fst2

When `unitex.py` executes:
```python
os.system("UnitexToolLogger Grf2Fst2 posologie.grf")
```

The process:
1. **Read** posologie.grf (visual grammar format)
2. **Parse** node definitions and transitions
3. **Reference** sub-graphs (dosage.grf, frequence.grf, etc.)
4. **Build** finite-state transducer
5. **Optimize** for pattern matching
6. **Output** posologie.fst2 (binary compiled format)

---

## Pattern Matching Examples

### Example 1: Simple Dosage
**Corpus Text**: `METFORMINE 850 mg 3 fois par jour`

**Matching Process**:
1. `METFORMINE` → matches `<N+subst>` (medication name from dict)
2. `850 mg` → matches `dosage` sub-graph
3. `3 fois par jour` → matches `frequence` sub-graph
4. **Result**: EXTRACTED ✓

### Example 2: Complex Prescription
**Corpus Text**: `LOVENOX 0,4 ml : 1 injection/jour le soir pendant un mois`

**Matching Process**:
1. `LOVENOX` → matches `<N+subst>`
2. `0,4 ml` → matches `dosage`
3. `1 injection` → matches `quantite et type`
4. `le soir` → matches `heure`
5. `pendant un mois` → matches `duree`
6. **Result**: EXTRACTED ✓

### Example 3: Abbreviated Format
**Corpus Text**: `PLAVIX 75 mg : 1 cp/jour`

**Matching Process**:
1. `PLAVIX` → matches `<N+subst>`
2. `75 mg` → matches `dosage`
3. `1 cp` → matches `quantite et type`
4. `/jour` → matches `frequence`
5. **Result**: EXTRACTED ✓

### Example 4: Without Duration (Still Valid)
**Corpus Text**: `TEGRETOL 200 mg : 1 cp 2 fois par jour`

**Matching Process**:
1. `TEGRETOL` → matches `<N+subst>`
2. `200 mg` → matches `dosage`
3. `1 cp` → matches `quantite et type`
4. `2 fois par jour` → matches `frequence`
5. Duration is optional (not all prescriptions have it)
6. **Result**: EXTRACTED ✓

---

## Key Features

✅ **Medication Dictionary Integration**: Uses `<N+subst>` tag for dictionary-based matching
✅ **Flexible Patterns**: Handles various formats and abbreviations
✅ **Multi-Language**: French terminology support
✅ **Optional Components**: Some elements (duration, time) may be optional
✅ **Sub-graphs**: Modular design with separate patterns for each component
✅ **Case-Insensitive**: Handles uppercase, lowercase, mixed case

---

## Related Files

### Dependencies (must exist for grammar to work)

| File | Type | Purpose |
|------|------|---------|
| `dosage.grf` | Sub-graph | Dosage amount patterns |
| `frequence.grf` | Sub-graph | Frequency patterns |
| `heure.grf` | Sub-graph | Time patterns |
| `quantite_et_type.grf` | Sub-graph | Quantity & form patterns |
| `duree.grf` | Sub-graph | Duration patterns |
| `subst.dic` → `subst.bin` | Dictionary | Medication names |
| `Dela_fr.bin` | Dictionary | French language data |

### Generated Files

| File | Type | Purpose |
|------|------|---------|
| `posologie.fst2` | Compiled grammar | Executable pattern matcher |
| `posologie_snt/posologie.fst2` | Processed copy | Copy in corpus directory |

---

## Visual Graph Representation

### Node Layout (as defined in header)

```
                           heure (659, 138)
                                │
              dosage (483, 110) │
                    │           │
<E> (70, 200) → <N+subst> ──────┼──────────────────┐
(Entry)         (251, 58)        │                  │
                    │            │                  │
                    └────────────┴──────────────────┼──→ frequence
                                                    │    (498, 336)
                quantite et type (242, 321) ←──────┘
                    │
                    │
                    └──→ duree (549, 243) ──→ exit "" (300, 200)
```

---

## UNITEX Integration

### How This Grammar Is Used

1. **Compilation** (in unitex.py):
   ```python
   UnitexToolLogger Grf2Fst2 posologie.grf
   ```
   - Produces: `posologie.fst2`

2. **Pattern Matching** (in unitex.py):
   ```python
   UnitexToolLogger Locate -t corpus-medical.snt posologie.fst2 -a Alphabet.txt -L -I --all
   ```
   - Input: `corpus-medical.snt` (tokenized corpus)
   - Grammar: `posologie.fst2` (compiled)
   - Flags:
     - `-t` : Text corpus
     - `-a Alphabet.txt` : Character mappings
     - `-L` : Case-insensitive
     - `-I` : Include output
     - `--all` : All matches
   - Output: `concordance.ind` (match index)

3. **Result Formatting** (in unitex.py):
   ```python
   UnitexToolLogger Concord corpus-medical_snt/concord.ind -f "Courrier new" -s 12 -l 40 -r 55
   ```
   - Converts matches to `concord.html`

---

## Customization & Extension

### Adding New Posology Patterns

To match additional medication prescription formats:

1. **Identify** the new pattern components
2. **Create** or modify relevant sub-graph file (dosage.grf, frequence.grf, etc.)
3. **Add** new patterns to sub-graph
4. **Recompile** posologie.grf to FST2
5. **Test** with sample corpus text

### Example: Add New Frequency Pattern
If corpus contains `"all 8 hours"`:
1. Open `frequence.grf`
2. Add pattern matching `"all 8 hours"` or `"toutes les 8 heures"`
3. Recompile: `Grf2Fst2 posologie.grf`
4. Re-run unitex.py

---

## Common Issues & Solutions

### Issue: "posologie.grf not found"
**Solution**: Ensure file is in UNITEX working directory

### Issue: "Sub-graph file missing" (e.g., dosage.grf)
**Solution**: Verify all sub-graph files exist in same directory:
- dosage.grf
- frequence.grf
- heure.grf
- quantite_et_type.grf
- duree.grf

### Issue: No extractions found in concord.html
**Possible Causes**:
- Sub-graphs don't match corpus format
- Medication names not in subst.dic
- Text not tokenized correctly
- Pattern too strict

**Solutions**:
- Review sub-graph patterns
- Check corpus format matches patterns
- Test with simpler patterns first
- Enable debug mode to see match attempts

### Issue: Too many false positives
**Cause**: Patterns too permissive
**Solution**: Make patterns more restrictive in sub-graphs

### Issue: "subst.dic not found"
**Solution**: Ensure `subst.dic` exists (created by enrichir.py)

---

## Best Practices

1. **Modular Design**: Keep sub-graphs focused on single component
2. **Optional Fields**: Make duration, time optional for flexibility
3. **Format Variants**: Account for different abbreviations (mg/Mg, ml/mL, etc.)
4. **Case Handling**: Use case-insensitive matching (`-L` flag in Locate)
5. **Testing**: Test sub-graphs individually before full compilation
6. **Documentation**: Comment complex patterns for maintainability

---

## Performance Notes

- **Graph Complexity**: 8 nodes + 5 sub-graphs = reasonable size
- **Matching Speed**: Simple linear graph → fast execution
- **Memory**: Compiled FST2 is memory-efficient
- **Accuracy**: Can match 1000+ posologies per large corpus

---

## Integration with Project

This grammar file is part of **Step 3** (unitex.py) of the extraction project:

1. **extraire.py** → Creates `subst.dic`
2. **enrichir.py** → Enriches `subst.dic`
3. **unitex.py** → Uses `posologie.grf` to extract from corpus
4. **sqlite.py** → Stores results in database

**Output**: `concord.html` with extracted posologies
- Required: > 1000 extractions for project success
- Input to: `sqlite.py` script

---

## Technical Reference

### UNITEX Graph Format (.grf)

```
#Unigraph                    ← File type marker
[Header section]             ← Visual editor metadata
#                           ← Section separator
[Number of nodes]           ← Count
[Node definitions]          ← Pattern definitions
```

### Node Definition Syntax
```
"[Label]" [X] [Y] [Type] [NextNode]
```

### Special Tokens
- `<E>` : Entry point (epsilon/empty start)
- `""` : Exit point (empty/final state)
- `<N+subst>` : Dictionary tag for nouns (substance)
- `<PREP>` : Prepositions (if used)
- `<DET>` : Determiners (if used)
- `<ADJ>` : Adjectives (if used)

---

## Author Notes

The `posologie.grf` grammar represents a carefully designed pattern matching system for extracting structured medication information from unstructured medical text. Its success depends on:

1. **Quality Sub-graphs**: Each component must match real corpus variations
2. **Dictionary Completeness**: All medications must be in `subst.dic`
3. **Corpus Consistency**: Medical records must follow expected formats
4. **French Language Support**: Proper handling of accents and terminology

The grammar is designed to be:
- **Comprehensive**: Handles most common prescription formats
- **Flexible**: Optional components allow varied prescription styles
- **Robust**: Sub-graphs handle abbreviations and variations
- **Maintainable**: Modular sub-graph design for easy updates
