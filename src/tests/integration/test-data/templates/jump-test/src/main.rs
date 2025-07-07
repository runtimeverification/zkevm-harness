{{ src_header }}

use revm_interpreter::InstructionResult;
use revm_interpreter::interpreter::{Contract, Interpreter, InterpreterResult, SharedMemory};
use revm_interpreter::interpreter_action::InterpreterAction;
use revm_interpreter::opcode::make_instruction_table;
use revm_interpreter::primitives::specification::CancunSpec;
use revm_interpreter::primitives::{address, Bytecode, Bytes, U256};
use revm_interpreter::DummyHost;

const JUMP_OPCODE: u8 = 0x56;
const JUMPDEST_OPCODE: u8 = 0x5b;

#[unsafe(no_mangle)]
pub static mut CODE: [u8; 32] = [0x01; 32];

#[unsafe(no_mangle)]
pub static mut CODE_SIZE: usize = 16;


fn main() {
    // Given

    // assume CODE_SIZE <= 32
    if unsafe { CODE_SIZE } > 32 {
        return
    }

    let input = Bytes::from([]);
    let bytecode_iter = unsafe {
        std::iter::once(&JUMP_OPCODE)
        .chain(CODE[..CODE_SIZE].iter())
        .chain(std::iter::once(&JUMPDEST_OPCODE))
    };
    let bytecode = Bytecode::new_raw(Bytes::from_iter(bytecode_iter));
    let target_address = address!("0x0000000000000000000000000000000000000001");
    let caller = address!("0x0000000000000000000000000000000000000002");
    let call_value = U256::ZERO;
    let contract = Contract::new(
        input,
        bytecode,
        None,
        target_address,
        None,
        caller,
        call_value,
    );
    let gas_limit = 100000;
    let mut interpreter = Interpreter::new(contract, gas_limit, false);

    let Ok(()) = interpreter.stack.push(U256::from(unsafe { CODE_SIZE } + 1)) else {
        panic!()
    };

    let memory = SharedMemory::new();
    let instruction_table = make_instruction_table::<DummyHost, CancunSpec>();
    let mut host = DummyHost::default();

    // When
    let action = interpreter.run(memory, &instruction_table, &mut host);

    // Then
    let InterpreterAction::Return {
        result: InterpreterResult {
            result: InstructionResult::Stop,
            output: _,
            gas: _,
        }
    } = action else {
        panic!()
    };
    if interpreter.program_counter() != unsafe { CODE_SIZE } + 3 { // STOP at the end
        panic!()
    }
}
