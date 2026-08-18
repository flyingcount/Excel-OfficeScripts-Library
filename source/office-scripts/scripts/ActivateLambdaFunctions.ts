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

  const headerBlock: (string | number | boolean)[][] = sheet.getRangeByIndexes(0, 0, 20, 3).getValues();
  let headerRow: number = -1;
  let r: number = 0;
  for (r = 0; r < headerBlock.length; r++) {
    const headerName: string = String(headerBlock[r][0]).trim().toLowerCase();
    const headerCode: string = String(headerBlock[r][1]).trim().toLowerCase();
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
  const dataRange: ExcelScript.Range = sheet.getRangeByIndexes(first, 0, rowCount, 3);
  const values: (string | number | boolean)[][] = dataRange.getValues();
  const formulas: string[][] = dataRange.getFormulas();

  const namedItems: ExcelScript.NamedItem[] = workbook.getNames();
  const namedItemNames: string[] = [];
  let n0: number = 0;
  for (n0 = 0; n0 < namedItems.length; n0++) {
    namedItemNames.push(namedItems[n0].getName().toUpperCase());
  }

  let activated: number = 0;
  const skipped: string[] = [];
  let i: number = 0;
  for (i = 0; i < rowCount; i++) {
    const row: number = first + i;
    if (row <= headerRow) {
      continue;
    }

    const name: string = String(values[i][0]).trim();
    let formula: string = String(formulas[i][1]).trim();
    if (formula === "" || formula.charAt(0) !== "=") {
      formula = String(values[i][1]).trim();
    }
    if (formula.charAt(0) === "'") {
      formula = formula.substring(1);
    }
    if (formula !== "" && formula.charAt(0) !== "=") {
      formula = "=" + formula;
    }
    const note: string = String(values[i][2]).trim();

    if (name === "" || name === "Name") {
      continue;
    }
    if (formula === "") {
      skipped.push(name + " (no Lambda code)");
      continue;
    }

    const nameUpper: string = name.toUpperCase();
    let foundIndex: number = -1;
    let n: number = 0;
    for (n = 0; n < namedItemNames.length; n++) {
      if (namedItemNames[n] === nameUpper) {
        foundIndex = n;
        break;
      }
    }
    if (foundIndex >= 0) {
      namedItems[foundIndex].setFormula(formula);
      namedItems[foundIndex].setComment(note);
    } else {
      const added: ExcelScript.NamedItem = workbook.addNamedItem(name, formula, note);
      namedItems.push(added);
      namedItemNames.push(nameUpper);
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
