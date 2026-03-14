package backend

import (
	"fmt"
	"log"
	"os"
	"path/filepath"
	"time"
)

type InstallerLogger struct {
	file *os.File
}

func NewLogger(targetDir string) (*InstallerLogger, error) {
	if err := os.MkdirAll(targetDir, 0755); err != nil {
		return nil, err
	}

	logPath := filepath.Join(targetDir, "install.log")
	file, err := os.OpenFile(logPath, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		return nil, err
	}

	return &InstallerLogger{file: file}, nil
}

func (l *InstallerLogger) Log(message string) {
	timestamp := time.Now().Format("2006-01-02 15:04:05")
	fmt.Fprintf(l.file, "[%s] %s\n", timestamp, message)
	log.Printf("[%s] %s", timestamp, message)
}

func (l *InstallerLogger) Close() {
	if l.file != nil {
		l.file.Close()
	}
}
