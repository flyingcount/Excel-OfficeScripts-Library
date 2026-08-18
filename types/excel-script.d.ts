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
    getNamedItems(): NamedItem[];
    addNamedItem(name: string, formula: string, comment?: string): NamedItem;
    getTable(name: string): Table;
  }

  interface NamedItem {
    getName(): string;
    getFormula(): string;
    delete(): void;
    setComment(comment: string): void;
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
    setPosition(position: number): void;
    setName(name: string): void;
    activate(): void;
    getCell(row: number, column: number): Range;
  }

  interface Range {
    getAddress(): string;
    getRowCount(): number;
    getColumnCount(): number;
    getCell(row: number, column: number): Range;
    getResizedRange(deltaRows: number, deltaColumns: number): Range;
    setValue(value: string | number | boolean): void;
    getValue(): string | number | boolean | undefined;
    getFormula(): string;
    getRowIndex(): number;
    getWorksheet(): Worksheet;
    setValues(values: (string | number | boolean)[][]): void;
    setNumberFormat(format: string): void;
    setHyperlink(hyperlink: RangeHyperlink): void;
    getFormat(): RangeFormat;
    getTables(): Table[];
    addConditionalFormat(type: ConditionalFormatType): ConditionalFormat;
    clearAllConditionalFormats(): void;
  }

  enum ConditionalFormatType {
    custom = "Custom"
  }

  interface ConditionalFormat {
    getCustom(): CustomConditionalFormat;
    setStopIfTrue(value: boolean): void;
  }

  interface CustomConditionalFormat {
    getRule(): ConditionalFormatRule;
    getFormat(): ConditionalRangeFormat;
  }

  interface ConditionalFormatRule {
    setFormula(formula: string): void;
  }

  interface ConditionalRangeFormat {
    getFill(): ConditionalRangeFill;
  }

  interface ConditionalRangeFill {
    setColor(color: string): void;
  }

  interface RangeHyperlink {
    address?: string;
    documentReference?: string;
    screenTip?: string;
    textToDisplay?: string;
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
