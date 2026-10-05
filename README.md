# Grade Lattice

A marksheet reader for BCA semesters that does not stop at SGPA. It finds the **credit traps**: subjects where a few marks cross a grade band and move the semester average more than a larger gain somewhere else.

Open `index.html` in a browser. No install, no server.

## What is unusual about it

Most CGPA calculators average what you already have. Grade Lattice asks a different question: *which next mark is worth the most?*

For every subject it computes:

- current grade band and points
- marks still needed to cross the next band
- SGPA swing if that band is crossed, weighted by credits
- **trap score** = SGPA swing / marks required

The recovery plan then spends a mark budget on the cheapest traps until a target SGPA is hit, or reports that the target is out of reach.

Grade scale used (10-point, common in Indian universities):

| Band | Marks | Points |
| --- | --- | --- |
| O | 90–100 | 10 |
| A+ | 80–89 | 9 |
| A | 70–79 | 8 |
| B+ | 60–69 | 7 |
| B | 50–59 | 6 |
| C | 40–49 | 5 |
| F | below 40 | 0 |

## Run the Python core

```bash
python3 lattice.py
```

`lattice.py` is the same rule set as the page, so the ranking can be checked without the browser.

## Sample

The page loads a Semester IV BCA sheet (Data Structures, DBMS, Operating Systems, Computer Networks, Discrete Mathematics, and the two labs). Edit any mark. The lattice and the recovery column update immediately.

## Stack

HTML, CSS, and JavaScript for the registrar-docket interface. Python 3 for the standalone checker. No frameworks.
