conda deactivate
PowerShell.exe .\venv\Scripts\activate
$pkgName = $args[0]
$appName = $args[1]
$depth = $args[2]
echo $pkgName $appName $depth
python --version
pip list
python run.py $pkgName $appName $depth