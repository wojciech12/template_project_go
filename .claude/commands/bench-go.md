---
description: "Run Go benchmarks with memory profiling"
argument-hint: "[benchmark pattern]"
---

go test -bench=${ARGUMENTS:-.} -benchmem -cpu=1,2,4
