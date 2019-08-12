Add-Type -AssemblyName System.DirectoryServices.AccountManagement;
$me = [System.DirectoryServices.AccountManagement.UserPrincipal]::Current

$ret = $env:ComputerName.ToString(), $env:UserDomain.ToString(), $me.Sid.ToString(), $me.Guid.ToString(), $me.Name.ToString(), $me.SamAccountName.ToString(), $me.DisplayName.ToString(), $me.EmailAddress.ToString(), $me.Description.ToString(), $me.GivenName.ToString()

return $ret
