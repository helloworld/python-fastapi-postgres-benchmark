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
    logFile, err := os.OpenFile(outputDir + fileName, os.O_CREATE | os.O_WRONLY | os.O_TRUNC, 0644)
    _, err = logFile.WriteString(fmt.Sprintf(format, args...))
    if err != nil {
        fmt.Printf("Error writing to log file: %v\n", err)
    }
    logFile.WriteString("\n")
    defer logFile.Close()
}

func TestAftSummaries(t *testing.T) {
    for i := 1; i <= 4; i++ {
        dutName := fmt.Sprintf("router%d", i)
        dut := ondatra.DUT(t, dutName)
        
        aftPath := gnmi.OC().NetworkInstance("default").Afts().State()
        aft := gnmi.Get(t, dut, aftPath)

        jsonData, err := ygot.EmitJSON(aft, &ygot.EmitJSONConfig{
            Indent: "  ",
        })

        if err != nil {
            t.Fatalf("Error marshalling summary to JSON: %v", err)
        } else {
            writeLog(dutName+".txt", jsonData)
        }
    }
}

func TestGetConfigs(t *testing.T) {
    for i := 1; i <= 4; i++ {
        dutName := fmt.Sprintf("router%d", i)
        dut := ondatra.DUT(t, dutName)
        
        // Get specific configuration components instead of the full config
        // This helps avoid schema validation issues
        interfacesPath := gnmi.OC().Interface("").State()
        routingPath := gnmi.OC().NetworkInstance("default").Protocol(oc.PolicyTypes_INSTALL_PROTOCOL_TYPE_BGP, "BGP").State()
        
        // Fetch configurations separately
        interfaces := gnmi.Get(t, dut, interfacesPath)
        routing := gnmi.Get(t, dut, routingPath)

        // Convert to JSON with proper indentation
        interfacesJSON, err := ygot.EmitJSON(interfaces, &ygot.EmitJSONConfig{
            Indent: "  ",
            SkipValidation: true,  // Skip strict validation
        })
        if err != nil {
            t.Logf("Warning marshalling interfaces to JSON: %v", err)
        } else {
            writeLog(fmt.Sprintf("%s_interfaces.txt", dutName), interfacesJSON)
        }

        routingJSON, err := ygot.EmitJSON(routing, &ygot.EmitJSONConfig{
            Indent: "  ",
            SkipValidation: true,  // Skip strict validation
        })
        if err != nil {
            t.Logf("Warning marshalling routing to JSON: %v", err)
        } else {
            writeLog(fmt.Sprintf("%s_routing.txt", dutName), routingJSON)
        }
    }
}
