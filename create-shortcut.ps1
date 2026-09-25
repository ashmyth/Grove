$WshShell = New-Object -ComObject WScript.Shell
$shortcutPath = [Environment]::GetFolderPath("Desktop") + "\Grove.lnk"
$targetPath = "powershell.exe"
$arguments = '-NoExit -ExecutionPolicy Bypass -File "E:\Downloads\Grove\launch-grove.ps1"'
$workingDirectory = "E:\Downloads\Grove"
$iconLocation = "E:\Downloads\Grove\frontend\public\favicon.svg"
$description = "Grove (GeoPrithvi-Agri) - Canal Command Advisory System"

$shortcut = $WshShell.CreateShortcut($shortcutPath)
$shortcut.TargetPath = $targetPath
$shortcut.Arguments = $arguments
$shortcut.WorkingDirectory = $workingDirectory
$shortcut.IconLocation = $iconLocation
$shortcut.Description = $description
$shortcut.Save()

Write-Host "Desktop shortcut created at: $shortcutPath" -ForegroundColor Green