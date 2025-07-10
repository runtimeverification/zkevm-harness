{{ src_header }}

use revm_interpreter::interpreter::{Contract, Interpreter, SharedMemory};
use revm_interpreter::interpreter_action::InterpreterAction;
use revm_interpreter::opcode::make_instruction_table;
use revm_interpreter::primitives::specification::CancunSpec;
use revm_interpreter::primitives::{address, Bytecode, Bytes, U256};
use revm_interpreter::DummyHost;

const OPCODES: [u8; 2] = [0x39, 0x00]; // CODECOPY, STOP

const MEMORY_SIZE: usize = 256;
const MAX_CODE_SIZE: usize = 32;

#[unsafe(no_mangle)]
pub static mut CODE: [u8; MAX_CODE_SIZE] = [
    0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f,
    0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1a, 0x1b, 0x1c, 0x1d, 0x1e, 0x1f,
];

#[unsafe(no_mangle)]
pub static mut CODE_SIZE: usize = 24;

#[unsafe(no_mangle)]
pub static mut DEST_OFFSET: usize = 8;

#[unsafe(no_mangle)]
pub static mut OFFSET: usize = 4;

#[unsafe(no_mangle)]
pub static mut SIZE: usize = 12;

#[unsafe(no_mangle)]
pub static mut INDEX: usize = 3;

fn main() {
    // Given

    unsafe {
        // assume CODE_SIZE + 2 <= MAX_CODE_SIZE
        if CODE_SIZE + 2 > MAX_CODE_SIZE {
            return;
        }

        // assume OFFSET <= usize::MAX - SIZE
        if OFFSET > usize::MAX - SIZE {
            return;
        }

        // assume OFFSET + SIZE <= CODE_SIZE + 2
        if OFFSET + SIZE > CODE_SIZE + 2 {
            return;
        }

        // assume DEST_OFFSET <= usize::MAX - SIZE
        if DEST_OFFSET > usize::MAX - SIZE {
            return;
        }

        // assume DEST_OFFEST + SIZE <= MEMORY_SIZE
        if DEST_OFFSET + SIZE > MEMORY_SIZE {
            return;
        }

        // assume INDEX < SIZE
        if INDEX >= SIZE {
            return;
        }
    }

    let input = Bytes::new();
    let bytecode_iter = unsafe { OPCODES.iter().chain(CODE[..CODE_SIZE].iter()) };
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

    let size = U256::from(unsafe { SIZE });
    let offset = U256::from(unsafe { OFFSET });
    let dest_offset = U256::from(unsafe { DEST_OFFSET });

    interpreter.stack.push(size).unwrap();
    interpreter.stack.push(offset).unwrap();
    interpreter.stack.push(dest_offset).unwrap();

    let memory = SharedMemory::new();
    let instruction_table = make_instruction_table::<DummyHost, CancunSpec>();
    let mut host = DummyHost::default();

    let expected = unsafe {
        let code_index = OFFSET + INDEX;
        if code_index < 2 {
            OPCODES[code_index]
        } else {
            CODE[code_index - 2]
        }
    };

    // When
    let action = interpreter.run(memory, &instruction_table, &mut host);

    // Then
    let InterpreterAction::Return { result: _ } = action else {
        panic!()
    };
    let actual = interpreter
        .shared_memory
        .get_byte(unsafe { DEST_OFFSET + INDEX });
    assert_eq!(actual, expected);
}
