{{ src_header }}

use revm_interpreter::interpreter::{Contract, Interpreter, SharedMemory};
use revm_interpreter::interpreter_action::InterpreterAction;
use revm_interpreter::opcode::make_instruction_table;
use revm_interpreter::primitives::specification::CancunSpec;
use revm_interpreter::primitives::{address, Bytecode, Bytes, U256};
use revm_interpreter::DummyHost;

#[unsafe(no_mangle)]
static OP1: [u8; 32] = [
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01,
];

#[unsafe(no_mangle)]
static OP2: [u8; 32] = [
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02,
];

#[unsafe(no_mangle)]
static mut RESULT: [u8; 32] = [0x00; 32];

fn main() {
    let mut _bytecode = [0u8; 67];
    _bytecode[0] = 0x7f; // PUSH32
    _bytecode[1..33].copy_from_slice(&OP1);
    _bytecode[33] = 0x7f; // PUSH32
    _bytecode[34..66].copy_from_slice(&OP2);
    _bytecode[66] = 0x01; // ADD

    let input = Bytes::from([]);
    let bytecode = Bytecode::new_raw(Bytes::from(_bytecode));
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

    let action = interpreter.run(memory, &instruction_table, &mut host);
    let InterpreterAction::Return { result: _ } = action else {
        panic!()
    };
    let Ok(sum) = interpreter.stack.peek(0) else {
        panic!()
    };
    unsafe {
        RESULT = sum.to_be_bytes();
    }
}
