# Version Notes

## Current Production Version: v2.2.1

**File:** `index.html`

**Status:** ✅ **Production-Ready** - Optimized for clean text extraction and embeddings

---

## Why v2.2.1 Over v2.3.2?

### TL;DR
**v2.2.1 produces cleaner text for embeddings.** v2.3.2 has more features but introduces text noise that degrades NLP quality.

### Quality Comparison

| Aspect | v2.2.1 | v2.3.2 | Winner |
|--------|--------|--------|--------|
| **Clean Text** | ✅ High | ❌ Low (link pollution) | **v2.2.1** |
| **Embedding Quality** | ✅ Excellent | ❌ Degraded (noise) | **v2.2.1** |
| **Link Preservation** | ❌ None | ⚠️ Too aggressive | **Neither** |
| **Footnote Handling** | ❌ None | ✅ Complete | v2.3.2 |
| **Table Integrity** | ✅ Clean | ❌ Header duplication | **v2.2.1** |
| **Word Integrity** | ⚠️ Some issues | ⚠️ Same issues | Tie |
| **Reference Lists** | ⚠️ Partial | ✅ Complete | v2.3.2 |

**Verdict:** For embeddings and NLP use cases, **v2.2.1 wins decisively**.

---

## Critical Regression in v2.3.2

### The Link Pollution Problem

```markdown
❌ BAD (v2.3.2):
[All patients underwent](https://doi.org/10.3390/jcm11102790) [their](https://doi.org/10.1016/j.jchf.2019.06.013) treatment.

✅ GOOD (v2.2.1):
All patients underwent their treatment.
```

**Why this is devastating for embeddings:**
- Common words like "their" get linked
- Sentence structure is broken
- Token sequences are corrupted
- Semantic meaning is obscured
- Embedding models see `[their](https://...)` instead of `their`

**Root cause:** The `matchLinksToText` function in v2.3.2 is too aggressive.

---

## Detailed Analysis

### 1️⃣ Structural Fidelity

**v2.3.2 Improvements:**
- ✅ Reference list fully preserved and numerically stable
- ✅ Supplementary references intact
- ✅ DOI strings preserved
- ✅ Figure captions retained with context
- ✅ Multi-page table continuity preserved

**This is stronger than v2.2.1 in bibliographic completeness.**

### 2️⃣ Regression: Inline Link Pollution

v2.3.2 introduces aggressive inline link injections:

- Inside sentences: `[All patients underwent](https://...)`
- Inside tables: Column headers hyperlinked
- On common words: `[their](https://...)`, `[the](https://...)`
- On column headers: `[Validation set](https://...)`

This **significantly reduces readability and clean-text utility**. v2.2.1 was cleaner.

### 3️⃣ Word Integrity

v2.3.2 still contains ligature and merge artifacts:

- `representamajor`
- `onascale`
- `onadaily`
- `discrim inatory`
- `elim ination`
- `conf idence`
- `f inancial`
- `comb ination`

**Neither version fully normalizes ligatures.** This is a shared weakness.

### 4️⃣ Tables

**v2.3.2 regressions:**
- Header duplication: `Training set [Validation set]` repeated
- Hyperlinked column headers
- Column alignment drift
- Inline DOI inside column header row

**v2.2.1 is cleaner** in table presentation.

### 5️⃣ Figures & Captions

Figure captions in v2.3.2 are preserved but sometimes partially merged with body text.

Example:
```
Model development and validation strategy. RPM, Remote patient management...
```

Still usable, but **less clean than v2.2.1**.

---

## Experimental Version: v2.3.2

**File:** `index_experimental.html`

**Status:** ⚠️ **Experimental** - Advanced features with known regressions

### What v2.3.2 Adds:

1. **Complete Footnote Pipeline (Tasks 1-5):**
   - Detects footnote markers `[1]`, `1)`, superscripts
   - Extracts footnote content from page bottoms
   - Matches markers to footnotes (smart mapping)
      - Removes footnote text from pages (prevents duplication)
   - Inserts standard markdown footnotes `[^1]`

2. **Header/Footer Removal:**
   - Detects repetitive headers/footers
   - Removes page numbers, DOIs, journal names

3. **Multi-Column Detection:**
   - Detects 2-column academic paper layouts
   - Correctly reads left-to-right column order

### What v2.3.2 Breaks:

1. **Inline Link Pollution:**
   - Aggressive link injection on common words
   - Degrades embedding quality

2. **Table Header Duplication:**
   - Headers duplicated and hyperlinked incorrectly

3. **Word-Splitting Artifacts:**
   - Same ligature issues as v2.2.1

---

## Future Roadmap

### Option B: Hybrid v2.4.0 (Planned)

Start from v2.2.1 (clean base) and add:

- ✅ **Optional** footnote detection (off by default)
- ✅ **Toggle** for link preservation
- ✅ Fix ligature issues properly
- ✅ No header duplication
- ✅ Clean text as default, features as opt-in

### Design Principles:

1. **Clean text is paramount** for embeddings
2. **Link pollution corrupts semantic meaning**
3. **Table headers should never be hyperlinked**
4. **Footnotes are nice-to-have, not essential**
5. **Features must not degrade base quality**

---

## File Guide

| File | Version | Status | Use Case |
|------|---------|--------|----------|
| `index.html` | v2.2.1 | ✅ Production | **Clean text extraction, embeddings, NLP** |
| `index_experimental.html` | v2.3.2 | ⚠️ Experimental | Testing footnote features, reference |
| `index_v2.2.1.html` | v2.2.1 | 📚 Archive | Backup of production version |
| `index_v2.3.1.html` | v2.3.2 | 📚 Archive | Complete v2.3.2 code (full implementation) |

---

## Recommendation

**Use `index.html` (v2.2.1) for:**
- Embedding generation
- RAG pipelines
- Clean text extraction
- Table preservation
- Production use

**Use `index_experimental.html` (v2.3.2) for:**
- Testing footnote detection
- Evaluating advanced features
- Reference for future development
- NOT for production embeddings

---

## Credits

Reversion decision made February 16, 2026 based on user analysis comparing embedding quality between versions.

**Key insight:** More features ≠ better quality for NLP use cases. Clean text extraction is more valuable than structural richness when text noise degrades semantic understanding.
