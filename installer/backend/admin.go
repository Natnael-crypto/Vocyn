package backend

import (
	"runtime"

	"golang.org/x/sys/windows"
)

// IsAdmin checks if the current process is running with administrator privileges on Windows.
func IsAdmin() bool {
	if runtime.GOOS != "windows" {
		return true
	}

	var token windows.Token
	// OpenProcessToken expects (Handle, uint32, *Token)
	err := windows.OpenProcessToken(windows.CurrentProcess(), windows.TOKEN_QUERY, &token)
	if err != nil {
		return false
	}
	defer token.Close()

	tokenUser, err := token.GetTokenUser()
	if err != nil {
		return false
	}

	return tokenUser.User.Sid.IsWellKnown(windows.WinBuiltinAdministratorsSid)
}

// RequestAdminRestart (Optional) could be implemented to restart with runas verb
// but usually installers are launched with admin rights from a wrapper or by user.
