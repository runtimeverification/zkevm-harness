{{ src_header }}

use revm_interpreter::interpreter::{Contract, Interpreter, SharedMemory};
use revm_interpreter::interpreter_action::InterpreterAction;
use revm_interpreter::opcode::make_instruction_table;
use revm_interpreter::primitives::specification::CancunSpec;
use revm_interpreter::primitives::{address, Bytecode, Bytes, U256};
use revm_interpreter::DummyHost;

static BIN_RUNTIME: {{ contract_bin_runtime }}

static INPUT: {{ contract_input }}

#[unsafe(no_mangle)]
static mut RESULT: [u8; 32] = [0x00; 32];

fn main() {
    let input = Bytes::from_static(&INPUT);
    let bin_runtime = Bytes::from_static(&BIN_RUNTIME);
    let bytecode = Bytecode::new_raw(bin_runtime);
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

    let mut host = DummyHost::default();
    let instruction_table = make_instruction_table::<DummyHost, CancunSpec>();

    let memory_in = SharedMemory::new();
    let action = interpreter.run(memory_in, &instruction_table, &mut host);
    let InterpreterAction::Return { result } = action else {
        panic!()
    };

    unsafe {
        RESULT.copy_from_slice(&result.output[..32]);
    }
}
