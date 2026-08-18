# Test: Table of contents

## Setup

1. Excel on the web (or desktop Automate) → **Automate** → **New Script**.
2. Paste `source/office-scripts/scripts/TableOfContents.ts`. Save as **Table of contents**.
3. Use a workbook with at least two worksheets (not already named **Table of Contents**). Include a sheet whose name has a space.

## Run

Run the script. Run it a second time.

## Expected

- Sheet **Table of Contents** is the first tab and is active.
- A1 is bold **Table of Contents**.
- A2:B2 are bold headers `#` and `Name`.
- One numbered row per other worksheet, in workbook order. Column B is a hyperlink; clicking it goes to A1 of that sheet.
- The TOC sheet is not listed in its own table.
- A second run still leaves a single **Table of Contents** sheet (replaced, not duplicated) and does not error on the name.
- A sheet name with a space still links correctly.
