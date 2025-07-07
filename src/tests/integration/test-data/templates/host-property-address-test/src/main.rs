{{ src_header }}

use revm_interpreter::interpreter::{Contract, Interpreter, SharedMemory};
use revm_interpreter::interpreter_action::InterpreterAction;
use revm_interpreter::opcode::make_instruction_table;
use revm_interpreter::primitives::specification::CancunSpec;
use revm_interpreter::primitives::{address, Address, Bytecode, Bytes, U256};
use revm_interpreter::DummyHost;

const OPCODE: u8 = {{ opcode }};

#[unsafe(no_mangle)]
pub static mut VALUE: [u8; 20] = [
    0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f,
    0x10, 0x11, 0x12, 0x13,
];

#[unsafe(no_mangle)]
pub static mut INDEX: usize = 11;

fn main() {
    // Given
    let input = Bytes::new();
    let bytecode = Bytecode::new_raw(Bytes::from([OPCODE]));
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

    host.{{ property }} = Address::from(unsafe { VALUE });

    let expected = unsafe {
        if INDEX < 20 {
            VALUE[19 - INDEX]
        } else {
            0x00
        }
    };

    // When
    let action = interpreter.run(memory, &instruction_table, &mut host);

    // Then
    let InterpreterAction::Return { result: _ } = action else {
        panic!()
    };
    let actual_u256 = interpreter.stack.pop().unwrap();
    let actual = actual_u256.byte(unsafe { INDEX });
    assert_eq!(actual, expected);
}
