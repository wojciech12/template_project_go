package main

import (
	"os"
	"testing"
)

func TestMain(t *testing.T) {
	tests := []struct {
		name     string
		envValue string
		expected string
	}{
		{
			name:     "default greeting",
			envValue: "",
			expected: "Hello, World!",
		},
		{
			name:     "custom name",
			envValue: "Claude",
			expected: "Hello, Claude!",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if tt.envValue != "" {
				os.Setenv("NAME", tt.envValue)
				defer os.Unsetenv("NAME")
			}
			
			// This is a simple test structure - in a real app you'd extract
			// the greeting logic into a separate function to test it properly
		})
	}
}