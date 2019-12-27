#include "llvm/CodeGen/MachineBasicBlock.h"


void MFunCFG(MachineFunction &MF)
{
    std::vector<MachineBasicBlock*> MBBVec;
    StringRef fileName(MF.getName().str() + ".dot");
    enum sys::fs::OpenFlags F_None;
    std::error_code error;
    raw_fd_ostream file(fileName, error, F_None);

    file << "digraph \"CFG for'" + MF.getName() + "\' function\" {\n";
    for (auto MBBI = MF.begin(); MBBI != MF.end(); MBBI++)
    {
        MachineBasicBlock* curMBB = &*MBBI;
        if (std::find(MBBVec.begin(), MBBVec.end(), curMBB) == MBBVec.end())
        {
            MBBVec.push_back(curMBB);
        }
        std::string curMBBName = MF.getName().str() + "_" +  curMBB->getName().str() + "_" + std::to_string(curMBB->getNumber());
        curMBBName = replaceChar(curMBBName, '.');
        file << "\t" << curMBBName << " " " [shape=record, label=\"{";
        file << curMBBName << ":\\l\\l";
        for (auto MII = curMBB->begin(); MII != curMBB->end(); ++MII)
        {
            MachineInstr &MI = *MII;
            std::string str;
            raw_string_ostream rso(str);
            MI.print(rso);
            std::string MIStr = rso.str();
            MIStr = transMean(MIStr, '<');
            MIStr = transMean(MIStr, '>');
            file << MIStr << "\\l\n";
        }
        file << "}\"];\n";
        for (MachineBasicBlock *SucMBB : curMBB->successors())
        {
            if (std::find(MBBVec.begin(), MBBVec.end(),  SucMBB) == MBBVec.end())
            {
                MBBVec.push_back(SucMBB);
            }
            std::string sucMBBName = MF.getName().str() + "_" + SucMBB->getName().str() + "_" +  std::to_string(SucMBB->getNumber());
            sucMBBName = replaceChar(sucMBBName, '.');
            file << "\t" << curMBBName << "-> " << sucMBBName << ";\n";
        }
    }
    file << "}\n";
    file.close();
}