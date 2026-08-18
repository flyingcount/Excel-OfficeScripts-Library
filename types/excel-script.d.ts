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
    getActiveWorksheet(): Worksheet;
    getSelectedRange(): Range;
    getActiveCell(): Range;
  }

  interface Worksheet {
    getName(): string;
    getVisibility(): SheetVisibility;
    getUsedRange(): Range | undefined;
    delete(): void;
    getRange(address?: string): Range;
    getRangeByIndexes(startRow: number, startColumn: number, rowCount: number, columnCount: number): Range;
    setShowGridlines(show: boolean): void;
    setTabColor(color: string | undefined): void;
  }

  interface Range {
    getAddress(): string;
    getRowCount(): number;
    getColumnCount(): number;
    setValues(values: (string | number | boolean)[][]): void;
    setNumberFormat(format: string): void;
    getFormat(): RangeFormat;
    getTables(): Table[];
  }

  interface Table {
    getRange(): Range;
    setPredefinedTableStyle(style: string): void;
  }

  interface RangeFormat {
    getFont(): Font;
    autofitColumns(): void;
    setColumnWidth(width: number): void;
  }

  interface Font {
    setBold(value: boolean): void;
    setSize(size: number): void;
  }
}
