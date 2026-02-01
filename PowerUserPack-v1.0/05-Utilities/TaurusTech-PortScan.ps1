param($Target="127.0.0.1")

1..1024 | ForEach-Object {
try {
$s = New-Object Net.Sockets.TcpClient
$s.Connect($Target, $)
if ($s.Connected) { "$ open" }
$s.Close()
} catch {}
}