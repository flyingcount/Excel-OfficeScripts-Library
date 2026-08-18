/**
 * Highlight Differences
 *
 * Applies conditional formatting to the selection.
 * Green (#97FFC6): ROUND(cell, 2) = 0
 * Red (#FFBDBD): ROUND(top-row cell of that column, 2) <> 0
 *
 * For a selection whose top-left is Q11, the rules are
 * =ROUND(Q11,2)=0 and =ROUND(Q$11,2)<>0.
 *
 * Automate → New Script → paste this file → Save → Run.
 */
function main(workbook: ExcelScript.Workbook): void {
  const range = workbook.getSelectedRange();
  range.clearAllConditionalFormats();

  const topLeft = a1(range.getCell(0, 0));
  const greenFormula = "=ROUND(" + topLeft + ",2)=0";
  const redFormula = "=ROUND(" + lockRow(topLeft) + ",2)<>0";

  const green = range.addConditionalFormat(ExcelScript.ConditionalFormatType.custom);
  green.getCustom().getRule().setFormula(greenFormula);
  green.getCustom().getFormat().getFill().setColor("#97FFC6");
  green.setStopIfTrue(true);

  const red = range.addConditionalFormat(ExcelScript.ConditionalFormatType.custom);
  red.getCustom().getRule().setFormula(redFormula);
  red.getCustom().getFormat().getFill().setColor("#FFBDBD");
}

function a1(range: ExcelScript.Range): string {
  let address = range.getAddress();
  const bang = address.lastIndexOf("!");
  if (bang >= 0) {
    address = address.substring(bang + 1);
  }
  return address.split("$").join("");
}

function lockRow(address: string): string {
  let i = 0;
  while (i < address.length) {
    const ch = address.charAt(i);
    if (ch < "A" || ch > "Z") {
      break;
    }
    i++;
  }
  return address.substring(0, i) + "$" + address.substring(i);
}
