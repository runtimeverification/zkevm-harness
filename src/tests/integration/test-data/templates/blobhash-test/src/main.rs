{{ src_header }}

use revm_interpreter::interpreter::{Contract, Interpreter, SharedMemory};
use revm_interpreter::interpreter_action::InterpreterAction;
use revm_interpreter::opcode::make_instruction_table;
use revm_interpreter::primitives::specification::CancunSpec;
use revm_interpreter::primitives::{address, Bytecode, Bytes, B256, U256};
use revm_interpreter::DummyHost;

const OPCODE: u8 = 0x49;
const BLOB_HASHES_LEN: usize = 256;

#[unsafe(no_mangle)]
pub static mut INDEX: usize = 1;

#[unsafe(no_mangle)]
pub static mut VALUE: [u8; 32] = [
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02,
];

fn main() {
    // Given

    // assume INDEX < BLOB_HASHES_LEN
    if unsafe { INDEX } >= BLOB_HASHES_LEN {
        return;
    }

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

    let index = U256::from(unsafe { INDEX });
    interpreter.stack.push(index).unwrap();

    let memory = SharedMemory::new();
    let instruction_table = make_instruction_table::<DummyHost, CancunSpec>();
    let mut host = DummyHost::default();

    let expected = B256::from(unsafe { VALUE });

    let mut blob_hashes: Vec<B256> = Vec::with_capacity(256);
    unsafe {
        blob_hashes.set_len(256);
    }
    blob_hashes[unsafe { INDEX }] = expected;
    host.env.tx.blob_hashes = blob_hashes;

    // When
    let action = interpreter.run(memory, &instruction_table, &mut host);

    // Then
    let InterpreterAction::Return { result: _ } = action else {
        panic!()
    };
    let actual_u256 = interpreter.stack.pop().unwrap();
    let actual = B256::from(actual_u256);
    assert_eq!(actual, expected);
}
