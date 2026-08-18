# Paul Lambda function library

Excel workbook synced in git: `Paul Lambda function library.xlsx`.

Rebuild from `source/lambda/functions` after you add a `.lambda` file:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/Build-LambdaWorkbook.ps1
```

Sheet **Lambda functions** holds Name, Lambda code, and Note. Select rows and run Automate script **Activate Lambda functions** to write them into Name Manager.

Sheet **Activate script** is the same TypeScript as `source/office-scripts/scripts/ActivateLambdaFunctions.ts`, for pasting into Automate.
