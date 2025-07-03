{{ src_header }}

use revm_interpreter::InstructionResult;
use revm_interpreter::interpreter::{
    Contract,
    Interpreter,
    InterpreterResult,
    SharedMemory,
};
use revm_interpreter::interpreter_action::InterpreterAction;
use revm_interpreter::opcode::make_instruction_table;
use revm_interpreter::primitives::specification::CancunSpec;
use revm_interpreter::primitives::{address, Bytecode, Bytes, U256};
use revm_interpreter::DummyHost;

#[unsafe(no_mangle)]
pub static mut OPCODE: u8 = 0xfe;

fn main() {
    // Given
    let input = Bytes::from([]);
    let bytecode = unsafe {
        Bytecode::new_raw(Bytes::from([OPCODE]))
    };
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

    let memory = SharedMemory::new();
    let instruction_table = make_instruction_table::<DummyHost, CancunSpec>();
    let mut host = DummyHost::default();

    // When
    let action = interpreter.run(memory, &instruction_table, &mut host);

    // Then
    let InterpreterAction::Return {
        result: InterpreterResult {
            result: InstructionResult::InvalidFEOpcode,
            output: _,
            gas: _,
        }
    } = action else {
        panic!()
    };
}
