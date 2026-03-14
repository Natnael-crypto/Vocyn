package backend

import (
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"syscall"
)

// CreateShortcut creates a Windows shortcut (.lnk) using PowerShell.
func CreateShortcut(targetPath, shortcutPath, description, iconPath string) error {
	dir := filepath.Dir(shortcutPath)
	if _, err := os.Stat(dir); os.IsNotExist(err) {
		if err := os.MkdirAll(dir, 0755); err != nil {
			return err
		}
	}

	psCommand := fmt.Sprintf(
		`$WshShell = New-Object -ComObject WScript.Shell; `+
			`$Shortcut = $WshShell.CreateShortcut('%s'); `+
			`$Shortcut.TargetPath = '%s'; `+
			`$Shortcut.Description = '%s'; `+
			`$Shortcut.IconLocation = '%s'; `+
			`$Shortcut.Save()`,
		shortcutPath, targetPath, description, iconPath,
	)

	cmd := exec.Command("powershell", "-Command", psCommand)
	cmd.SysProcAttr = &syscall.SysProcAttr{HideWindow: true}
	if output, err := cmd.CombinedOutput(); err != nil {
		return fmt.Errorf("powershell error: %v, output: %s", err, string(output))
	}

	return nil
}

// GetDesktopPath returns the absolute path to the current user's desktop.
func GetDesktopPath() string {
	home, _ := os.UserHomeDir()
	return filepath.Join(home, "Desktop")
}

// GetStartMenuPath returns the absolute path to the current user's Start Menu programs folder.
func GetStartMenuPath() string {
	home, _ := os.UserHomeDir()
	return filepath.Join(home, "AppData", "Roaming", "Microsoft", "Windows", "Start Menu", "Programs")
}
