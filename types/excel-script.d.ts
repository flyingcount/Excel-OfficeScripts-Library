/**
 * Minimal ExcelScript typings for editor checks.
 * Excel Automate provides the full API at run time.
 */
declare namespace ExcelScript {
  enum SheetVisibility {
    visible = "Visible",
    hidden = "Hidden",
    veryHidden = "VeryHidden"
  }

  interface Workbook {
    getWorksheets(): Worksheet[];
    getWorksheet(name: string): Worksheet | undefined;
    addWorksheet(name?: string): Worksheet;
  }

  interface Worksheet {
    getName(): string;
    getVisibility(): SheetVisibility;
    getUsedRange(): Range | undefined;
    delete(): void;
    getRange(address: string): Range;
    getRangeByIndexes(startRow: number, startColumn: number, rowCount: number, columnCount: number): Range;
  }

  interface Range {
    getAddress(): string;
    getRowCount(): number;
    getColumnCount(): number;
    setValues(values: (string | number | boolean)[][]): void;
    getFormat(): RangeFormat;
  }

  interface RangeFormat {
    getFont(): Font;
    autofitColumns(): void;
  }

  interface Font {
    setBold(value: boolean): void;
  }
}
