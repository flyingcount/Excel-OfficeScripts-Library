/**
 * Format Table
 *
 * On the active sheet: show gridlines and set the tab colour to green.
 * If the active cell is in a table: font size 10, TableStyleLight14,
 * and column width 56 on the table only (not every column on the sheet).
 *
 * Automate → New Script → paste this file → Save → Run.
 */
function main(workbook: ExcelScript.Workbook): void {
  const ws = workbook.getActiveWorksheet();
  ws.setShowGridlines(true);
  ws.setTabColor("Green");

  const tables = workbook.getActiveCell().getTables();
  if (tables.length === 0) {
    console.log("Active cell is not within a table.");
    return;
  }

  const table = tables[0];
  const tableRange = table.getRange();
  tableRange.getFormat().getFont().setSize(10);
  tableRange.getFormat().setColumnWidth(56);
  table.setPredefinedTableStyle("TableStyleLight14");
}
