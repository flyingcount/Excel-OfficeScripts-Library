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
  const sheetName: string = "Lambda functions";
  const worksheets: ExcelScript.Worksheet[] = workbook.getWorksheets();
  let sheet: ExcelScript.Worksheet = worksheets[0];
  let foundSheet: boolean = false;
  for (let w: number = 0; w < worksheets.length; w++) {
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

  const headerRow: number = findHeaderRow(sheet);
  if (headerRow < 0) {
    throw new Error('Could not find a header row with Name, Lambda code, Note.');
  }

  const first: number = selected.getRowIndex();
  const rowCount: number = selected.getRowCount();
  let activated: number = 0;
  const skipped: string[] = [];

  for (let i: number = 0; i < rowCount; i++) {
    const row: number = first + i;
    if (row <= headerRow) {
      continue;
    }

    const name: string = cellText(sheet, row, 0);
    const formula: string = lambdaFormula(sheet, row, 1);
    const note: string = cellText(sheet, row, 2);

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
  for (let r: number = 0; r < 20; r++) {
    const a: string = cellText(sheet, r, 0).toLowerCase();
    const b: string = cellText(sheet, r, 1).toLowerCase();
    if (a === "name" && b.indexOf("lambda") >= 0) {
      return r;
    }
  }
  return -1;
}

function cellText(sheet: ExcelScript.Worksheet, row: number, column: number): string {
  const cell: ExcelScript.Range = sheet.getCell(row, column);
  const value: string | number | boolean = cell.getValue();
  return String(value).trim();
}

function lambdaFormula(sheet: ExcelScript.Worksheet, row: number, column: number): string {
  const cell: ExcelScript.Range = sheet.getCell(row, column);
  let formula: string = "";
  const asFormula: string = cell.getFormula();
  if (asFormula && asFormula.charAt(0) === "=") {
    formula = asFormula.trim();
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
  const items: ExcelScript.NamedItem[] = workbook.getNamedItems();
  for (let i: number = 0; i < items.length; i++) {
    const named: ExcelScript.NamedItem = items[i];
    if (named.getName() === name) {
      named.delete();
      break;
    }
  }
  const item: ExcelScript.NamedItem = workbook.addNamedItem(name, formula);
  if (note !== "") {
    item.setComment(note);
  }
}
