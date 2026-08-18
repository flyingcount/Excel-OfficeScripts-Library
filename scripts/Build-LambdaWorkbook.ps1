#Requires -Version 5.1
<#
.SYNOPSIS
  Rebuild workbook/Paul Lambda function library.xlsx from source/lambda/functions.

.DESCRIPTION
  Reads every *.lambda file, writes sheet "Lambda functions" (instructions +
  Name / Lambda code / Note table) and sheet "Activate script" (Office Script
  source). Requires Excel on Windows. Close the workbook first if it is open.
#>
[CmdletBinding()]
param(
    [string]$RepoRoot = ''
)

if (-not $RepoRoot) {
    $here = $PSScriptRoot
    if (-not $here -and $MyInvocation.MyCommand.Path) {
        $here = Split-Path -Parent $MyInvocation.MyCommand.Path
    }
    if ($here) {
        $RepoRoot = (Resolve-Path (Join-Path $here '..')).Path
    } else {
        $RepoRoot = (Get-Location).Path
    }
}

$ErrorActionPreference = 'Stop'
$lambdaDir = Join-Path $RepoRoot 'source\lambda\functions'
$scriptPath = Join-Path $RepoRoot 'source\office-scripts\scripts\ActivateLambdaFunctions.ts'
$outDir = Join-Path $RepoRoot 'workbook'
$outPath = Join-Path $outDir 'Paul Lambda function library.xlsx'

if (-not (Test-Path $lambdaDir)) {
    throw "Lambda folder not found: $lambdaDir"
}

function Get-LambdaRecords {
    $records = @()
    Get-ChildItem -LiteralPath $lambdaDir -Filter '*.lambda' | Sort-Object Name | ForEach-Object {
        $name = $null
        $description = $null
        $formulaLines = New-Object System.Collections.Generic.List[string]
        $inFormula = $false
        foreach ($line in Get-Content -LiteralPath $_.FullName) {
            if ($line -match '^Name:\s*(.+)$') {
                $name = $Matches[1].Trim()
                continue
            }
            if ($line -match '^Description:\s*(.+)$') {
                $description = $Matches[1].Trim()
                continue
            }
            if ($line -match '^(Parameters|Docs):') {
                continue
            }
            if (-not $inFormula -and $line -match '^\s*=') {
                $inFormula = $true
            }
            if ($inFormula) {
                [void]$formulaLines.Add($line.TrimEnd())
            }
        }
        $formula = ($formulaLines -join '').Trim()
        if (-not $name -or -not $formula) {
            Write-Warning "Skipping $($_.Name): missing Name or =LAMBDA line."
            return
        }
        $records += [pscustomobject]@{
            Name        = $name
            Formula     = $formula
            Description = $description
        }
    }
    return $records
}

$records = @(Get-LambdaRecords)
if ($records.Count -eq 0) {
    throw "No lambda files parsed from $lambdaDir"
}

$scriptText = ''
if (Test-Path -LiteralPath $scriptPath) {
    $scriptText = Get-Content -LiteralPath $scriptPath -Raw
}

if (-not (Test-Path $outDir)) {
    New-Item -ItemType Directory -Path $outDir | Out-Null
}

$instructions = @(
    'Paul Lambda function library',
    'To activate a function: select one or more rows in the table below, then Automate -> Activate Lambda functions.',
    'The script adds (or replaces) those names in Name Manager so you can use them in formulas, for example =ROUND2(A1).',
    'First-time setup: Automate -> New Script -> paste sheet "Activate script" (or source/office-scripts/scripts/ActivateLambdaFunctions.ts) -> Save as Activate Lambda functions. After adding a .lambda file in git, rebuild this workbook with scripts/Build-LambdaWorkbook.ps1.'
)

$excel = $null
$wb = $null
try {
    $excel = New-Object -ComObject Excel.Application
    $excel.Visible = $false
    $excel.DisplayAlerts = $false
    $wb = $excel.Workbooks.Add()

    while ($wb.Worksheets.Count -lt 2) {
        [void]$wb.Worksheets.Add()
    }

    $ws = $wb.Worksheets.Item(1)
    $ws.Name = 'Lambda functions'

    $ws.Range('A1').Value2 = $instructions[0]
    $ws.Range('A1').Font.Bold = $true
    $ws.Range('A1').Font.Size = 16
    $ws.Range('A2').Value2 = $instructions[1]
    $ws.Range('A3').Value2 = $instructions[2]
    $ws.Range('A4').Value2 = $instructions[3]
    $ws.Range('A2:A4').Font.Size = 11
    foreach ($r in 1..4) {
        $ws.Range("A${r}:C${r}").Merge() | Out-Null
        $ws.Range("A${r}").WrapText = $true
    }
    $ws.Range('A1').Font.Bold = $true
    $ws.Range('A1').Font.Size = 16
    $ws.Rows.Item(1).RowHeight = 24
    $ws.Rows.Item(2).RowHeight = 32
    $ws.Rows.Item(3).RowHeight = 32
    $ws.Rows.Item(4).RowHeight = 48
    $ws.Range('A2:A4').Font.Size = 11

    $headerRow = 6
    $ws.Cells.Item($headerRow, 1).Value2 = 'Name'
    $ws.Cells.Item($headerRow, 2).Value2 = 'Lambda code'
    $ws.Cells.Item($headerRow, 3).Value2 = 'Note'
    $ws.Range("A${headerRow}:C${headerRow}").Font.Bold = $true

    $row = $headerRow + 1
    foreach ($rec in $records) {
        $ws.Cells.Item($row, 1).NumberFormat = '@'
        $ws.Cells.Item($row, 1).Value2 = $rec.Name
        $ws.Cells.Item($row, 2).NumberFormat = '@'
        $ws.Cells.Item($row, 2).Value2 = [string]$rec.Formula
        $ws.Cells.Item($row, 3).NumberFormat = '@'
        $ws.Cells.Item($row, 3).Value2 = [string]$rec.Description
        $ws.Rows.Item($row).WrapText = $true
        $row++
    }
    $lastData = $row - 1

    $listRange = $ws.Range("A${headerRow}:C${lastData}")
    $lo = $ws.ListObjects.Add(1, $listRange, $null, 1)
    $lo.Name = 'tblLambdaFunctions'
    $lo.TableStyle = 'TableStyleMedium2'

    $ws.Columns.Item(1).ColumnWidth = 28
    $ws.Columns.Item(2).ColumnWidth = 80
    $ws.Columns.Item(3).ColumnWidth = 55
    $ws.Range("B$($headerRow + 1):B$lastData").WrapText = $true
    $ws.Range("C$($headerRow + 1):C$lastData").WrapText = $true
    $ws.Activate()
    $excel.ActiveWindow.SplitRow = $headerRow
    $excel.ActiveWindow.FreezePanes = $true

    $wsScript = $wb.Worksheets.Item(2)
    $wsScript.Name = 'Activate script'
    $wsScript.Range('A1').Value2 = 'Paste this into Automate -> New Script. Save as Activate Lambda functions. Then use sheet Lambda functions.'
    $wsScript.Range('A1').Font.Bold = $true
    $wsScript.Range('A1').WrapText = $true
    $wsScript.Rows.Item(1).RowHeight = 36
    $wsScript.Columns.Item(1).ColumnWidth = 120
    $wsScript.Range('A2').NumberFormat = '@'
    $wsScript.Range('A2').Value2 = $scriptText
    $wsScript.Range('A2').WrapText = $true
    $wsScript.Rows.Item(2).RowHeight = 400

    $ws.Activate()

    if (Test-Path -LiteralPath $outPath) {
        Remove-Item -LiteralPath $outPath -Force
    }
    $xlOpenXMLWorkbook = 51
    $wb.SaveAs($outPath, $xlOpenXMLWorkbook)
    Write-Host "Wrote $outPath ($($records.Count) functions)"
}
finally {
    if ($wb) {
        $wb.Close($false) | Out-Null
        [void][Runtime.InteropServices.Marshal]::ReleaseComObject($wb)
    }
    if ($excel) {
        $excel.Quit() | Out-Null
        [void][Runtime.InteropServices.Marshal]::ReleaseComObject($excel)
    }
    [GC]::Collect()
    [GC]::WaitForPendingFinalizers()
}
