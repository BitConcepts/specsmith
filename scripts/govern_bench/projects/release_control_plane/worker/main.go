package main

import (
	"errors"
	"time"
)

// Release is the worker's incomplete view of the shared contract.
type Release struct {
	ID        string `json:"id"`
	Service   string `json:"service"`
	CreatedAt string `json:"created_at"`
}

// NormalizePlan must be completed as part of T29.
func NormalizePlan(raw []byte) (Release, error) {
	return Release{CreatedAt: time.Now().UTC().Format(time.RFC3339)}, errors.New("not implemented")
}

func main() {}
