requires "riscv-semantics/riscv.md"

module RISC0
  imports RISCV

  rule <instrs> ECALL => .K ... </instrs>
       <regs> 5 |-> 2 ... </regs>  // SOFTWARE

  rule <instrs> ECALL => .K ... </instrs>
       <regs> 5 |-> 3 ... </regs>  // SHA
endmodule
