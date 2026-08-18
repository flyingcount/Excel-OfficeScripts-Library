# Source

`scripts/` holds one TypeScript file per Automate script. Each file must define:

```typescript
function main(workbook: ExcelScript.Workbook): void {
  // ...
}
```

`shared/` holds helpers that are **copied** into a script. Office Scripts cannot import modules from this folder.

Do not put VBA (`.bas`) or Power Query (`.pq`) here.
