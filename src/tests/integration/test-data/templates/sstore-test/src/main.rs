{{ src_header }}

use revm_interpreter::DummyHost;
use revm_interpreter::interpreter::{Contract, Interpreter, SharedMemory};
use revm_interpreter::interpreter_action::InterpreterAction;
use revm_interpreter::opcode::make_instruction_table;
use revm_interpreter::primitives::specification::CancunSpec;
use revm_interpreter::primitives::{B256, Bytecode, Bytes, HashMap, U256, address};

#[unsafe(no_mangle)]
static KEY: [u8; 32] = [
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01,
];

#[unsafe(no_mangle)]
static VALUE: [u8; 32] = [
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xde, 0xad, 0xbe, 0xef,
];

#[unsafe(no_mangle)]
static mut STACK_ADDR: usize = 0;

#[unsafe(no_mangle)]
static mut STORAGE_ADDR: usize = 0;

fn main() {
    // Given
    let mut _bytecode = [0u8; 67];
    _bytecode[0] = 0x7f; // PUSH32
    _bytecode[1..33].copy_from_slice(&VALUE);
    _bytecode[33] = 0x7f; // PUSH32
    _bytecode[34..66].copy_from_slice(&KEY);
    _bytecode[66] = 0x55; // SSTORE

    let key: U256 = B256::from(&KEY).into();
    let expected_value = B256::from(&VALUE).into();

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

    unsafe {
        STACK_ADDR = &interpreter.stack as *const _ as usize;
    }

    let memory = SharedMemory::new();
    let instruction_table = make_instruction_table::<DummyHost, CancunSpec>();
    let mut host = DummyHost::default();

    host.storage = HashMap::with_capacity(4096);

    unsafe {
        STORAGE_ADDR = &interpreter.stack as *const _ as usize;
    }

    // When
    let action = interpreter.run(memory, &instruction_table, &mut host);

    // Then
    let InterpreterAction::Return { result: _ } = action else {
        panic!()
    };

    let Some(actual_value) = host.storage.get(&key) else {
        panic!()
    };
    assert_eq!(actual_value, &expected_value);
}
