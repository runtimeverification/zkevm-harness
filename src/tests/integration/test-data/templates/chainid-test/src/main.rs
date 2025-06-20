{{ src_header }}

use revm_interpreter::interpreter::{Contract, Interpreter, SharedMemory};
use revm_interpreter::interpreter_action::InterpreterAction;
use revm_interpreter::opcode::make_instruction_table;
use revm_interpreter::primitives::specification::CancunSpec;
use revm_interpreter::primitives::{address, Bytecode, Bytes, U256};
use revm_interpreter::DummyHost;

const OPCODE: u8 = 0x46;

#[unsafe(no_mangle)]
pub static mut VALUE: u64 = 1;

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

    let memory = SharedMemory::new();
    let instruction_table = make_instruction_table::<DummyHost, CancunSpec>();
    let mut host = DummyHost::default();

    host.env.cfg.chain_id = unsafe { VALUE };

    // When
    let action = interpreter.run(memory, &instruction_table, &mut host);

    // Then
    let InterpreterAction::Return { result: _ } = action else {
        panic!()
    };
    let Ok(res) = interpreter.stack.pop() else {
        panic!()
    };
    let Ok(gas_price) = u64::try_from(res) else {
        panic!()
    };
    if gas_price != unsafe { VALUE } {
        panic!()
    }
}
