package gnmi_test

import (
    "fmt"
    "os"
    "testing"
    "... ygot"
    "... gnmi"
    "... knebind/init/init"
    "... ondatra"
)

var (
    outputDir = "src/cloud/...ondatra/tests/gnmi"
)

func TestMain(m *testing.M) {
    ondatra.RunTests(m, knebind.Init)
}

func writeLog(fileName string, format string, args ...any) {
    logFile, err := os.OpenFile(outputDir+fileName, os.O_CREATE|os.O_WRONLY|os.O_TRUNC, 0644)
    _, err = logFile.WriteString(fmt.Sprintf(format, args...))
    if err != nil {
        fmt.Printf("Error writing to log file: %v\n", err)
    }
    logFile.WriteString("\n")
    defer logFile.Close()
}

func TestGetConfigsV2(t *testing.T) {
    for i := 1; i <= 4; i++ {
        dutName := fmt.Sprintf("router%d", i)
        dut := ondatra.DUT(t, dutName)
        
        // Get the raw configuration using a simple path
        configPath := gnmi.OC().Root()
        config := gnmi.Get(t, dut, configPath)

        // Convert to JSON with relaxed validation
        jsonData, err := ygot.EmitJSON(config, &ygot.EmitJSONConfig{
            Indent: "  ",
            SkipValidation: true,
            RFC7951Config: true,  // Use RFC7951 encoding for better compatibility
        })

        if err != nil {
            t.Logf("Warning while marshalling config to JSON: %v", err)
        } else {
            writeLog(fmt.Sprintf("%s_full_config.txt", dutName), jsonData)
        }
    }
}