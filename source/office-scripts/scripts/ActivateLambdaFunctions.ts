/**
 * Activate Lambda functions
 *
 * On sheet **Lambda functions**, select one or more table rows and Run.
 * Each selected Name is written to this workbook's Name Manager
 * (replaced if it already exists) using the Lambda code column.
 *
 * Automate → New Script → paste this file → Save as **Activate Lambda functions**.
 * GitHub and the catalog workbook do not update Automate. Replace the whole script.
 * Office Scripts only reliably runs code inside main, so helpers are inlined.
 */
function main(workbook: ExcelScript.Workbook): void {
  const sheetName: string = "Lambda functions";
  const worksheets: ExcelScript.Worksheet[] = workbook.getWorksheets();
  let sheet: ExcelScript.Worksheet = worksheets[0];
  let foundSheet: boolean = false;
  let w: number = 0;
  for (w = 0; w < worksheets.length; w++) {
    if (worksheets[w].getName() === sheetName) {
      sheet = worksheets[w];
      foundSheet = true;
      break;
    }
  }
  if (!foundSheet) {
    throw new Error('Sheet "Lambda functions" was not found.');
  }

  const selected: ExcelScript.Range = workbook.getSelectedRange();
  if (selected.getWorksheet().getName() !== sheetName) {
    throw new Error('Select one or more rows on "Lambda functions", then run this script.');
  }

  let headerRow: number = -1;
  let r: number = 0;
  for (r = 0; r < 20; r++) {
    const headerName: string = String(sheet.getCell(r, 0).getValue()).trim().toLowerCase();
    const headerCode: string = String(sheet.getCell(r, 1).getValue()).trim().toLowerCase();
    if (headerName === "name" && headerCode.indexOf("lambda") >= 0) {
      headerRow = r;
      break;
    }
  }
  if (headerRow < 0) {
    throw new Error('Could not find a header row with Name, Lambda code, Note.');
  }

  const first: number = selected.getRowIndex();
  const rowCount: number = selected.getRowCount();
  let activated: number = 0;
  const skipped: string[] = [];
  let i: number = 0;
  for (i = 0; i < rowCount; i++) {
    const row: number = first + i;
    if (row <= headerRow) {
      continue;
    }

    const name: string = String(sheet.getCell(row, 0).getValue()).trim();
    const codeCell: ExcelScript.Range = sheet.getCell(row, 1);
    let formula: string = String(codeCell.getFormula()).trim();
    if (formula === "" || formula.charAt(0) !== "=") {
      formula = String(codeCell.getValue()).trim();
    }
    if (formula.charAt(0) === "'") {
      formula = formula.substring(1);
    }
    if (formula !== "" && formula.charAt(0) !== "=") {
      formula = "=" + formula;
    }
    const note: string = String(sheet.getCell(row, 2).getValue()).trim();

    if (name === "" || name === "Name") {
      continue;
    }
    if (formula === "") {
      skipped.push(name + " (no Lambda code)");
      continue;
    }

    // Office Scripts collection is getNames(), not getNamedItems().
    const namedItems: ExcelScript.NamedItem[] = workbook.getNames();
    let replaced: boolean = false;
    let n: number = 0;
    for (n = 0; n < namedItems.length; n++) {
      if (namedItems[n].getName().toUpperCase() === name.toUpperCase()) {
        namedItems[n].setFormula(formula);
        namedItems[n].setComment(note);
        replaced = true;
        break;
      }
    }
    if (!replaced) {
      workbook.addNamedItem(name, formula, note);
    }
    activated++;
  }

  if (activated === 0) {
    throw new Error('No function rows were selected. Select rows under the Name / Lambda code / Note header.');
  }

  console.log("Activated " + activated + " named function(s) in Name Manager.");
  if (skipped.length > 0) {
    console.log("Skipped: " + skipped.join("; "));
  }
}
