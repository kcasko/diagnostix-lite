(Get-FileHash -Algorithm SHA256 $args[0]).Hash

Usage:
powershell -file TaurusTech-FileHash.ps1 myfile.iso