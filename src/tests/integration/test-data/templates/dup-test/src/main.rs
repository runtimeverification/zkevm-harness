{{ src_header }}

use revm_interpreter::interpreter::{Contract, Interpreter, SharedMemory};
use revm_interpreter::interpreter_action::InterpreterAction;
use revm_interpreter::opcode::make_instruction_table;
use revm_interpreter::primitives::specification::CancunSpec;
use revm_interpreter::primitives::{address, Bytecode, Bytes, U256};
use revm_interpreter::DummyHost;

const N: u8 = {{ n }};

#[unsafe(no_mangle)]
pub static mut OPCODE: u8 = {{ opcode }};

#[unsafe(no_mangle)]
pub static mut OP0: [u8; 32] = [
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01,
];

#[unsafe(no_mangle)]
pub static mut STATE: u8 = 0;

#[unsafe(no_mangle)]
pub static mut STACK_ADDR: usize = 0;

#[unsafe(no_mangle)]
pub static mut RESULT: [u8; 32] = [0x00; 32];

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

    unsafe {
        STACK_ADDR = &interpreter.stack as *const _ as usize;
    }

    stack_addr_ready();

    for _ in 1..N {
        let Ok(()) = interpreter.stack.push(U256::ZERO) else {
            panic!()
        };
    }

    unsafe {
        let Ok(()) = interpreter.stack.push(U256::from_be_bytes(OP0)) else {
            panic!()
        };
    }

    stack_ready();

    let memory = SharedMemory::new();
    let instruction_table = make_instruction_table::<DummyHost, CancunSpec>();
    let mut host = DummyHost::default();

    setup_done();

    // When
    let action = interpreter.run(memory, &instruction_table, &mut host);

    // Then
    let InterpreterAction::Return { result: _ } = action else {
        panic!()
    };
    let Ok(res) = interpreter.stack.pop() else {
        panic!()
    };
    unsafe {
        RESULT = res.to_be_bytes();
    }
}

#[unsafe(no_mangle)]
#[inline(never)]
fn stack_addr_ready() -> () {
    unsafe {
        STATE = 1;
    }
}

#[unsafe(no_mangle)]
#[inline(never)]
fn stack_ready() -> () {
    unsafe {
        STATE = 2;
    }
}

#[unsafe(no_mangle)]
#[inline(never)]
fn setup_done() -> () {
    unsafe {
        STATE = 3;
    }
}
