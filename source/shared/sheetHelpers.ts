/**
 * Replace an existing worksheet of the same name, then return the new sheet.
 * Copy this function into a script; do not import it from Automate.
 */
function replaceWorksheet(workbook: ExcelScript.Workbook, name: string): ExcelScript.Worksheet {
  const existing = workbook.getWorksheet(name);
  if (existing) {
    existing.delete();
  }
  return workbook.addWorksheet(name);
}
