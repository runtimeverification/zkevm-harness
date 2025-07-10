{{ src_header }}

use revm_interpreter::interpreter::{Contract, Interpreter, InterpreterResult, SharedMemory};
use revm_interpreter::interpreter_action::InterpreterAction;
use revm_interpreter::opcode::make_instruction_table;
use revm_interpreter::primitives::specification::CancunSpec;
use revm_interpreter::primitives::{address, Bytecode, Bytes, U256};
use revm_interpreter::DummyHost;
use revm_interpreter::InstructionResult;

const CODE_PREFIX: u8 = 0x56; // JUMP
const CODE_SUFFIX: [u8; 2] = [0x5b, 0x00]; // JUMPDEST, STOP

const MAX_CODE_SIZE: usize = 32;

#[unsafe(no_mangle)]
pub static mut CODE: [u8; MAX_CODE_SIZE] = [0x01; MAX_CODE_SIZE];

#[unsafe(no_mangle)]
pub static mut CODE_SIZE: usize = 16;

fn main() {
    // Given

    // assume CODE_SIZE <= MAX_CODE_SIZE
    if unsafe { CODE_SIZE } > MAX_CODE_SIZE {
        return;
    }

    let input = Bytes::new();
    let bytecode_iter = unsafe {
        std::iter::once(&CODE_PREFIX)
            .chain(CODE[..CODE_SIZE].iter())
            .chain(CODE_SUFFIX.iter())
    };
    let bytecode = Bytecode::new_raw(Bytes::from_iter(bytecode_iter));
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

    let counter = U256::from(unsafe { CODE_SIZE } + 1);
    interpreter.stack.push(counter).unwrap();

    let memory = SharedMemory::new();
    let instruction_table = make_instruction_table::<DummyHost, CancunSpec>();
    let mut host = DummyHost::default();

    let expected = unsafe { CODE_SIZE } + 3;

    // When
    let action = interpreter.run(memory, &instruction_table, &mut host);

    // Then
    let InterpreterAction::Return {
        result:
            InterpreterResult {
                result: InstructionResult::Stop,
                output: _,
                gas: _,
            },
    } = action
    else {
        panic!()
    };
    let actual = interpreter.program_counter();
    assert_eq!(actual, expected);
}
