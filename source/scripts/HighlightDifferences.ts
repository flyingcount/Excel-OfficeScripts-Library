/**
 * Highlight Differences
 *
 * Applies conditional formatting to the selection. Values that match to 2
 * decimal places fill green (#97FFC6); otherwise red (#FFBDBD).
 *
 * Comparison:
 * - 2 columns: each row, left vs right
 * - 2 rows (and not 2 columns): each column, top vs bottom
 * - 1 column: each cell vs the first cell
 * - otherwise: each cell vs the first column of the same row
 *
 * Automate → New Script → paste this file → Save → Run.
 */
function main(workbook: ExcelScript.Workbook): void {
  const range = workbook.getSelectedRange();
  range.clearAllConditionalFormats();

  const equalFormula = equalToTwoDecimalsFormula(range);
  const unequalFormula = "=NOT(" + equalFormula.substring(1) + ")";

  const green = range.addConditionalFormat(ExcelScript.ConditionalFormatType.custom);
  green.getCustom().getRule().setFormula(equalFormula);
  green.getCustom().getFormat().getFill().setColor("#97FFC6");

  const red = range.addConditionalFormat(ExcelScript.ConditionalFormatType.custom);
  red.getCustom().getRule().setFormula(unequalFormula);
  red.getCustom().getFormat().getFill().setColor("#FFBDBD");
}

function equalToTwoDecimalsFormula(range: ExcelScript.Range): string {
  const rows = range.getRowCount();
  const cols = range.getColumnCount();
  const topLeft = a1(range.getCell(0, 0));

  if (cols === 2) {
    const left = lockColumn(topLeft);
    const right = lockColumn(a1(range.getCell(0, 1)));
    return roundEqualFormula(left, right);
  }

  if (rows === 2) {
    const top = lockRow(topLeft);
    const bottom = lockRow(a1(range.getCell(1, 0)));
    return roundEqualFormula(top, bottom);
  }

  if (cols === 1) {
    return roundEqualFormula(topLeft, lockRow(topLeft));
  }

  return roundEqualFormula(topLeft, lockColumn(topLeft));
}

function roundEqualFormula(a: string, b: string): string {
  return "=AND(ISNUMBER(" + a + "),ISNUMBER(" + b + "),ROUND(" + a + ",2)=ROUND(" + b + ",2))";
}

function a1(range: ExcelScript.Range): string {
  let address = range.getAddress();
  const bang = address.lastIndexOf("!");
  if (bang >= 0) {
    address = address.substring(bang + 1);
  }
  return address.split("$").join("");
}

function lockColumn(address: string): string {
  return "$" + address;
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
