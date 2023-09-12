$third_octet = '231' # Changes every time

$public_prefix = '192.168'
$private_prefix = '172.16'

$public_final_octets = '120','121','122'
$private_final_octets = '10','11','12','13','14','82','83'

$ips = @()
foreach($oct in $public_final_octets) {
    $ips += $public_prefix + '.' + $third_octet + '.' + $oct
}
foreach($oct in $private_final_octets) {
    $ips += $private_prefix + '.' + $third_octet + '.' + $oct
}

foreach($ip in $ips) {
    1..1024 | % {echo ((New-Object Net.Sockets.TcpClient).Connect($ip, $_)) "$ip TCP port $_ is open"} 2>$null
}
