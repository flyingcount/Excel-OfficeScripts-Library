/**
 * Activate Lambda functions
 *
 * On sheet **Lambda functions**, select one or more table rows and Run.
 * Each selected Name is written to this workbook's Name Manager
 * (replaced if it already exists) using the Lambda code column.
 *
 * Automate → New Script → paste this file → Save as **Activate Lambda functions**.
 */
function main(workbook: ExcelScript.Workbook): void {
  const sheetName = "Lambda functions";
  const sheet = workbook.getWorksheet(sheetName);
  if (!sheet) {
    throw new Error('Sheet "Lambda functions" was not found.');
  }

  const selected = workbook.getSelectedRange();
  if (selected.getWorksheet().getName() !== sheetName) {
    throw new Error('Select one or more rows on "Lambda functions", then run this script.');
  }

  const headerRow = findHeaderRow(sheet);
  if (headerRow < 0) {
    throw new Error('Could not find a header row with Name, Lambda code, Note.');
  }

  const first = selected.getRowIndex();
  const rowCount = selected.getRowCount();
  let activated = 0;
  const skipped: string[] = [];

  for (let i = 0; i < rowCount; i++) {
    const row = first + i;
    if (row <= headerRow) {
      continue;
    }

    const name = cellText(sheet, row, 0);
    const formula = lambdaFormula(sheet, row, 1);
    const note = cellText(sheet, row, 2);

    if (name === "" || name === "Name") {
      continue;
    }
    if (formula === "") {
      skipped.push(name + " (no Lambda code)");
      continue;
    }

    replaceNamedItem(workbook, name, formula, note);
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

function findHeaderRow(sheet: ExcelScript.Worksheet): number {
  for (let r = 0; r < 20; r++) {
    const a = cellText(sheet, r, 0).toLowerCase();
    const b = cellText(sheet, r, 1).toLowerCase();
    if (a === "name" && b.indexOf("lambda") >= 0) {
      return r;
    }
  }
  return -1;
}

function cellText(sheet: ExcelScript.Worksheet, row: number, column: number): string {
  const cell = sheet.getCell(row, column);
  const value = cell.getValue();
  if (value === undefined || value === null) {
    return "";
  }
  return String(value).trim();
}

function lambdaFormula(sheet: ExcelScript.Worksheet, row: number, column: number): string {
  const cell = sheet.getCell(row, column);
  let formula = "";
  const asFormula = cell.getFormula();
  if (asFormula && String(asFormula).charAt(0) === "=") {
    formula = String(asFormula).trim();
  } else {
    formula = cellText(sheet, row, column);
  }
  if (formula.charAt(0) === "'") {
    formula = formula.substring(1);
  }
  if (formula !== "" && formula.charAt(0) !== "=") {
    formula = "=" + formula;
  }
  return formula;
}

function replaceNamedItem(
  workbook: ExcelScript.Workbook,
  name: string,
  formula: string,
  note: string
): void {
  const items = workbook.getNamedItems();
  for (let i = 0; i < items.length; i++) {
    if (items[i].getName() === name) {
      items[i].delete();
      break;
    }
  }
  const item = workbook.addNamedItem(name, formula);
  if (note && note !== "") {
    item.setComment(note);
  }
}
