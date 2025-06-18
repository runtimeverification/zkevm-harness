{{ src_header }}

use revm_interpreter::interpreter::{Contract, Interpreter, SharedMemory};
use revm_interpreter::interpreter_action::InterpreterAction;
use revm_interpreter::opcode::make_instruction_table;
use revm_interpreter::primitives::specification::CancunSpec;
use revm_interpreter::primitives::{address, Bytecode, Bytes, HashMap, U256};
use revm_interpreter::DummyHost;

#[unsafe(no_mangle)]
pub static mut OPCODE: u8 = 0x55;

#[unsafe(no_mangle)]
pub static mut KEY: [u8; 32] = [
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01,
];

#[unsafe(no_mangle)]
pub static mut VALUE: [u8; 32] = [
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xde, 0xad, 0xbe, 0xef,
];

#[unsafe(no_mangle)]
pub static mut STACK_ADDR: usize = 0;

#[unsafe(no_mangle)]
pub static mut STORAGE_ADDR: usize = 0;

#[unsafe(no_mangle)]
pub static STORAGE_SIZE: usize = 256;

#[unsafe(no_mangle)]
pub static mut RESULT: [u8; 32] = [0; 32];

fn main() {
    let input = Bytes::from([]);
    let bytecode = Bytecode::new_raw(Bytes::from([unsafe { OPCODE }]));
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

    let Ok(()) = interpreter.stack.push(U256::from_be_bytes(unsafe { VALUE })) else {
        panic!()
    };
    let Ok(()) = interpreter.stack.push(U256::from_be_bytes(unsafe { KEY })) else {
        panic!()
    };

    let memory = SharedMemory::new();
    let instruction_table = make_instruction_table::<DummyHost, CancunSpec>();
    let mut host = DummyHost::default();

    host.storage = HashMap::with_capacity(STORAGE_SIZE);

    unsafe {
        STORAGE_ADDR = &host.storage as *const _ as usize;
    }

    // When
    let action = interpreter.run(memory, &instruction_table, &mut host);

    // Then
    let InterpreterAction::Return { result: _ } = action else {
        panic!()
    };

    let key = U256::from_be_bytes(unsafe { KEY });
    let Some(value) = host.storage.get(&key) else {
        panic!()
    };
    unsafe {
        RESULT = value.to_be_bytes();
    }
}
