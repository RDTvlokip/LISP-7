# 🔐 LISP-7: Linguistic Irreversible Scrambling Protocol

**Destructive Semantic Encoding — A New Paradigm for Information Security**

What if security relied not on ever-more-complex mathematical locks, but on **destroying the message itself** in semantic noise that can't be reconstructed?

---

## 📋 Quick Facts

- **Novel Paradigm:** Destructive Semantic Encoding (DSE)
- **7 Progressive Levels:** Vowel removal → Alphabet mutation
- **Level-7 Innovation:** Unique random alphabet key per compression
- **Complexity:** ~10^60 states (22 words), 10^35 years brute-force @ exascale
- **Information Loss:** 79.4% per word (true destruction, non-reversible)
- **Validation:** 40K+ French phrases tested

---

## 🎯 Core Idea

Unlike **RSA/AES** (reversible), LISP-7 **intentionally destroys** information:

```
Plain:     "La technologie moderne"
L7 #1:     "qpm nmx mme dmp vpm J"  (key: abcd...xyz)
L7 #2:     "tua vam aaj wau gua B"  (key: wxyz...abc)
L7 #3:     "nsl mlw llt cls dsl Z"  (key: qrst...mno)

Same plaintext → completely different outputs every time
```

**Without dictionary + alphabet key:** Impossible to reconstruct.

---

## 📚 Paper & Citation

**Zenodo:** https://doi.org/10.5281/zenodo.17638778

```bibtex
@misc{charlet_2025_lisp7,
  author       = {Charlet, Théo},
  title        = {LISP-7: Linguistic Irreversible Scrambling Protocol
                  — Destructive Semantic Encoding (DSE)},
  year         = 2025,
  doi          = {10.5281/zenodo.17638778},
  url          = {https://doi.org/10.5281/zenodo.17638778}
}
```

---

## 🔧 7 Levels

| Level | Operation | Security |
|-------|-----------|----------|
| 1️⃣ | Vowel removal | Low |
| 2️⃣ | Extended removal | Low |
| 3️⃣ | Triadic extraction | Medium |
| 4️⃣ | Chaos markers | High |
| 5️⃣ | Letter permutation | Very High |
| 6️⃣ | Word-order scrambling | Extreme |
| 7️⃣ | **Alphabet mutation** | **Maximum** |

---

## 🛡️ Security Model

**Two-Key Lock:**
```
✅ Correct compressed + Correct key → Decompression works
❌ Correct compressed + Wrong key  → FAIL
❌ Wrong compressed + Correct key  → FAIL
❌ No dictionary                   → Impossible
```

---

## 📊 Complexity

**State Space (Real Case: 22-word phrase)**
- Level 7: ~7.67 × 10^60 configurations

**Brute-Force @ Exascale (10^18 ops/sec)**
- Level 7: **2.43 × 10^35 years** (10^25 × age of universe)

---

## 💡 Use Cases

- 🗃️ Archival security with semantic destruction
- 🔒 Privacy through irreversibility (not encryption)
- 🛡️ Multi-layer defense (DSE + AES-256)
- 📄 AI-resistant obfuscation

---

## 🚫 Limitations

- Dictionary loss = irreversible
- Domain-specific effectiveness
- Metadata leakage (word lengths)
- Short words (< 3 chars) need handling

---

## 📖 How It Works

```
INPUT: "La technologie moderne revolutionne notre societe"

Level 3:  Extract 1st + mid + last per word
Level 5:  Randomize letter order per word
Level 6:  Scramble word positions
Level 7:  Apply unique alphabet substitution (K_α)

OUTPUT:   "sgd adr ddy idg lgd H" (key: jpkmduqvanchylifbsrgowextz)
```

**Decompression:** Dictionary lookup + key reversal = 100% accurate

## 🎯 Quick Demo

Visit the web interface and try the example already in the database:
- Compressed text
- Level 7 alphabet key
- Decompress it to see the original message

This demonstrates the two-key lock: without BOTH the compressed text AND the alphabet key, reconstruction is impossible.

---

## ⚡ Philosophy

> *The future of security: ever-more complex mathematical locks… or making the message disappear into semantic noise that can't be reconstructed?*

LISP-7 answers: **Destroy, don't hide.** 🔐

---

**Author:** Théo Charlet (RDTvlokip)
**License:** CC BY-SA 4.0
