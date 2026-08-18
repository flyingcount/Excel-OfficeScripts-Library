/**
 * Table of contents
 *
 * Inserts sheet **Table of Contents** at the front of the workbook, with
 * a numbered hyperlink to A1 of every other worksheet. Replaces an existing
 * TOC sheet so a second run does not fail on the name.
 *
 * Automate → New Script → paste this file → Save → Run.
 */
function main(workbook: ExcelScript.Workbook): void {
  const tocName = "Table of Contents";
  const tocSheet = replaceWorksheet(workbook, tocName);
  tocSheet.setPosition(0);

  tocSheet.getRange("A1").setValue("Table of Contents");
  tocSheet.getRange("A1").getFormat().getFont().setBold(true);

  tocSheet.getRange("A2:B2").setValues([["#", "Name"]]);
  tocSheet.getRange("A2:B2").getFormat().getFont().setBold(true);

  const worksheets = workbook.getWorksheets();
  let row = 3;
  let index = 1;
  for (let i = 0; i < worksheets.length; i++) {
    const sheet = worksheets[i];
    const name = sheet.getName();
    if (name === tocName) {
      continue;
    }

    tocSheet.getRange("A" + row).setValue(index);
    tocSheet.getRange("B" + row).setHyperlink({
      textToDisplay: name,
      documentReference: "'" + name.split("'").join("''") + "'!A1"
    });
    row++;
    index++;
  }

  const filled = tocSheet.getUsedRange();
  if (filled) {
    filled.getFormat().autofitColumns();
  }
  tocSheet.activate();
}

function replaceWorksheet(workbook: ExcelScript.Workbook, name: string): ExcelScript.Worksheet {
  const existing = workbook.getWorksheet(name);
  if (existing) {
    existing.delete();
  }
  return workbook.addWorksheet(name);
}
