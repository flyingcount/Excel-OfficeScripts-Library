/**
 * Paul's format
 *
 * Applies one of Paul's custom number formats to the selected range.
 * Automate shows a dropdown for the style (default 0dp).
 *
 * Automate → New Script → paste this file → Save → Run.
 */
function main(
  workbook: ExcelScript.Workbook,
  style:
    | "0dp"
    | "2dp"
    | "0dp Colour"
    | "2dp Colour"
    | "0dp k"
    | "1dp m"
    | "Date dd-mm-yyyy"
    | "Date dd-mmm-yyyy" = "0dp"
): void {
  const format = paulsNumberFormat(style);
  if (format === "") {
    return;
  }
  workbook.getSelectedRange().setNumberFormat(format);
}

function paulsNumberFormat(
  style:
    | "0dp"
    | "2dp"
    | "0dp Colour"
    | "2dp Colour"
    | "0dp k"
    | "1dp m"
    | "Date dd-mm-yyyy"
    | "Date dd-mmm-yyyy"
): string {
  switch (style) {
    case "0dp":
      return "#,##0_);(#,##0); -";
    case "2dp":
      return "#,##0.00_);(#,##0.00); -";
    case "0dp Colour":
      return "#,##0_);[red](#,##0); -";
    case "2dp Colour":
      return "#,##0.00_);[red](#,##0.00); -";
    case "0dp k":
      return '#,##0, "k"';
    case "1dp m":
      return '#,##0.0,, "m"';
    case "Date dd-mm-yyyy":
      return "dd-mm-yyyy";
    case "Date dd-mmm-yyyy":
      return "dd-mmm-yyyy";
    default:
      return "";
  }
}
