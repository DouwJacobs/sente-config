// SPDX-License-Identifier: GPL-3.0-only
package tests

import (
	"encoding/json"
	"os"
	"path/filepath"
	"regexp"
	"strings"
	"testing"

	"github.com/DouwJacobs/sente-config/internal/matcher"
)

type rule struct {
	Pattern   string `json:"pattern"`
	Direction string `json:"direction"`
	Merchant  string `json:"merchant"`
	Category  string `json:"category"`
}
type pack struct {
	MerchantRules []rule `json:"merchant_rules"`
	Rules         []rule `json:"rules"`
}
type fixture struct {
	File       string   `json:"file"`
	Collection string   `json:"collection"`
	Pattern    string   `json:"pattern"`
	Target     string   `json:"target"`
	Matches    []string `json:"matches"`
	NonMatches []string `json:"non_matches"`
}

func key(file, collection, pattern string) string {
	return file + "\x00" + collection + "\x00" + pattern
}
func read(t *testing.T, path string, target any) {
	t.Helper()
	data, err := os.ReadFile(path)
	if err != nil {
		t.Fatal(err)
	}
	if err := json.Unmarshal(data, target); err != nil {
		t.Fatal(err)
	}
}

func TestPublishedPatterns(t *testing.T) {
	paths, err := filepath.Glob("../packs/*.json")
	if err != nil {
		t.Fatal(err)
	}
	paths = append(paths, "../sente.json")
	rules := map[string]rule{}
	for _, path := range paths {
		var p pack
		read(t, path, &p)
		file := strings.TrimPrefix(filepath.ToSlash(path), "../")
		for collection, items := range map[string][]rule{"merchant_rules": p.MerchantRules, "rules": p.Rules} {
			for _, r := range items {
				// Community regexes must compile in Go even though the runtime can fall back to literals.
				if strings.ContainsAny(r.Pattern, `.*+?^$[](){}\`) {
					if _, err := regexp.Compile("(?i)" + r.Pattern); err != nil {
						t.Fatalf("%s: invalid regexp: %v", file, err)
					}
				}
				rules[key(file, collection, r.Pattern)] = r
			}
		}
	}
	var fixtures []fixture
	read(t, "matching.json", &fixtures)
	seen := map[string]bool{}
	for _, f := range fixtures {
		k := key(f.File, f.Collection, f.Pattern)
		r, ok := rules[k]
		if !ok {
			t.Fatalf("orphan fixture for %s %s", f.File, f.Pattern)
		}
		if seen[k] {
			t.Fatalf("duplicate fixture: %s", k)
		}
		seen[k] = true
		target := r.Merchant
		if f.Collection == "rules" {
			target = r.Category
		}
		if f.Target != target {
			t.Fatalf("fixture target %q differs from published %q", f.Target, target)
		}
		if len(f.Matches) == 0 || len(f.NonMatches) == 0 {
			t.Fatalf("positive/negative examples required for %s", k)
		}
		t.Run(f.File+"/"+f.Pattern, func(t *testing.T) {
			for _, description := range f.Matches {
				if !matcher.MatchPattern(description, r.Pattern) {
					t.Errorf("should match %q", description)
				}
			}
			for _, description := range f.NonMatches {
				if matcher.MatchPattern(description, r.Pattern) {
					t.Errorf("should not match %q", description)
				}
			}
			if r.Direction != "debit" && r.Direction != "credit" {
				t.Errorf("explicit direction required")
			}
		})
	}
	for k := range rules {
		if !seen[k] {
			t.Errorf("missing synthetic fixture: %s", k)
		}
	}
}

func TestMatcherSnapshotSemantics(t *testing.T) {
	for _, c := range []struct {
		description, pattern string
		expected             bool
	}{
		{"Example   Store", "example store", true},
		{"PURCH Example", "Example or Other", true},
		{"PURCH Other", "Example, Other", true},
		{"PURCH OTHER", "Example|Other", true},
		{"A123", "(A[0-9]+|B[0-9]+)", true},
		{"A123", "A[0-9]+|B[0-9]+", false},
		{"unrelated", "", false},
	} {
		if matcher.MatchPattern(c.description, c.pattern) != c.expected {
			t.Errorf("pattern %q with %q", c.pattern, c.description)
		}
	}
}
