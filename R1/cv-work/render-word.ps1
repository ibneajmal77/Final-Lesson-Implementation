param([string]$InputDocx='D:\Final-Lesson-Implementation\R1\Muhammad-Awais-CV-Updated.docx', [string]$OutputPdf='D:\Final-Lesson-Implementation\R1\cv-work\updated-qa.pdf')
$ErrorActionPreference = 'Stop'
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
try {
    $doc = $word.Documents.Open($InputDocx, $false, $true)
    $doc.Repaginate()
    Write-Output ('Pages: ' + $doc.ComputeStatistics(2))
    $doc.ExportAsFixedFormat($OutputPdf,17)
    $doc.Close(0)
} finally { $word.Quit() }
