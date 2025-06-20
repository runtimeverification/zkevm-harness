{{ src_header }}

use revm_interpreter::interpreter::{Contract, Interpreter, SharedMemory};
use revm_interpreter::interpreter_action::InterpreterAction;
use revm_interpreter::opcode::make_instruction_table;
use revm_interpreter::primitives::specification::CancunSpec;
use revm_interpreter::primitives::{address, B256, Bytecode, Bytes, U256};
use revm_interpreter::DummyHost;

const OPCODE: u8 = 0x49;

#[unsafe(no_mangle)]
pub static mut INDEX: u8 = 0x01;

#[unsafe(no_mangle)]
pub static mut VALUE: [u8; 32] = [
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02,
];


fn main() {
    // Given
    let input = Bytes::from([]);
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

    let Ok(()) = interpreter.stack.push(U256::from(unsafe { INDEX })) else {
        panic!()
    };

    let memory = SharedMemory::new();
    let instruction_table = make_instruction_table::<DummyHost, CancunSpec>();
    let mut host = DummyHost::default();

    let mut blob_hashes: Vec<B256> = Vec::with_capacity(256);
    unsafe {
        blob_hashes.set_len(256);
    }
    let expected = B256::from(unsafe { VALUE });
    blob_hashes[usize::from(unsafe { INDEX })] = expected;
    host.env.tx.blob_hashes = blob_hashes;


    // When
    let action = interpreter.run(memory, &instruction_table, &mut host);

    // Then
    let InterpreterAction::Return { result: _ } = action else {
        panic!()
    };
    let Ok(res) = interpreter.stack.pop() else {
        panic!()
    };
    let actual = B256::from(res);
    if actual != expected {
        panic!()
    }
}
