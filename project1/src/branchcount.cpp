/* Custom Pintools for MO601 - Project 1
 Author : Alberto Arruda de Oliveira
 
 */
#include <iostream>
#include <fstream>
#include "pin.H"

ofstream OutFile;

// Stores the number of branches
static UINT64 totalcount = 0;
static UINT64 isbranch = 0;
static UINT64 notbranch = 0;

// This function is called before every instruction is executed
VOID counttotal() { totalcount++; }
VOID countbranches() { isbranch++; }
VOID countnotbranches() { notbranch++; }
    
// Pin calls this function every time a new instruction is encountered
VOID Instruction(INS ins, VOID *v)
{
    // Count the total of instructions
    INS_InsertCall(ins, IPOINT_BEFORE, (AFUNPTR)counttotal, IARG_END);
    
    // Call the function that count branches if the instruction is a branch,
    // and the one that count notbranches if it's not a branch
    if(INS_IsBranch(ins)){
        INS_InsertCall(ins, IPOINT_BEFORE, (AFUNPTR)countbranches, IARG_END);
    }
    else{
        INS_InsertCall(ins, IPOINT_BEFORE, (AFUNPTR)countnotbranches, IARG_END);
    }
}

KNOB<string> KnobOutputFile(KNOB_MODE_WRITEONCE, "pintool",
    "o", "branchcount.out", "specify output file name");

// Called by the end of the application
VOID Done(INT32 code, VOID *v)
{
    // Write to a file since cout and cerr maybe closed by the application
    OutFile.setf(ios::showbase);
    OutFile << "Total Count: " << totalcount << endl;
    OutFile << "Branch Count: " << isbranch << endl;
    OutFile << "Not Branch Count: " << notbranch << endl;
    OutFile.close();
}

/* ===================================================================== */
/* Print Help Message                                                    */
/* ===================================================================== */

INT32 Usage()
{
    cerr << "Counts the number of branches executed by the program" << endl;
    cerr << endl << KNOB_BASE::StringKnobSummary() << endl;
    return -1;
}

/* ===================================================================== */
/* Main                                                                  */
/* ===================================================================== */
/*   argc, argv are the entire command line: pin -t <toolname> -- ...    */
/* ===================================================================== */

int main(int argc, char * argv[])
{
    // Initialize pin
    if (PIN_Init(argc, argv)) return Usage();

    OutFile.open(KnobOutputFile.Value().c_str());

    // Register Instruction to be called to instrument instructions
    INS_AddInstrumentFunction(Instruction, 0);

    // Register Fini to be called when the application exits
    PIN_AddFiniFunction(Done, 0);
    
    // Start the program, never returns
    PIN_StartProgram();
    
    return 0;
}
