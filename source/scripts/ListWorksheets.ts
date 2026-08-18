/**
 * List worksheets
 *
 * Writes sheet **Worksheets** with name, visibility, and used-range size
 * for every worksheet in the workbook (except the output sheet).
 *
 * Automate → New Script → paste this file → Save → Run.
 */
function main(workbook: ExcelScript.Workbook): void {
  const outName = "Worksheets";
  const out = replaceWorksheet(workbook, outName);

  const header: (string | number | boolean)[] = [
    "Name",
    "Visibility",
    "Used range",
    "Row count",
    "Column count"
  ];
  const rows: (string | number | boolean)[][] = [header];

  const sheets = workbook.getWorksheets();
  for (let i = 0; i < sheets.length; i++) {
    const sheet = sheets[i];
    if (sheet.getName() === outName) {
      continue;
    }

    const used = sheet.getUsedRange();
    let address = "";
    let rowCount = 0;
    let columnCount = 0;
    if (used) {
      address = used.getAddress();
      rowCount = used.getRowCount();
      columnCount = used.getColumnCount();
    }

    rows.push([
      sheet.getName(),
      visibilityLabel(sheet.getVisibility()),
      address,
      rowCount,
      columnCount
    ]);
  }

  out.getRangeByIndexes(0, 0, rows.length, header.length).setValues(rows);
  out.getRange("1:1").getFormat().getFont().setBold(true);
  const filled = out.getUsedRange();
  if (filled) {
    filled.getFormat().autofitColumns();
  }
}

function replaceWorksheet(workbook: ExcelScript.Workbook, name: string): ExcelScript.Worksheet {
  const existing = workbook.getWorksheet(name);
  if (existing) {
    existing.delete();
  }
  return workbook.addWorksheet(name);
}

function visibilityLabel(value: ExcelScript.SheetVisibility): string {
  if (value === ExcelScript.SheetVisibility.visible) {
    return "Visible";
  }
  if (value === ExcelScript.SheetVisibility.hidden) {
    return "Hidden";
  }
  if (value === ExcelScript.SheetVisibility.veryHidden) {
    return "Very hidden";
  }
  return String(value);
}
