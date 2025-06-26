{{ src_header }}

use revm_interpreter::interpreter::{Contract, Interpreter, SharedMemory};
use revm_interpreter::interpreter_action::InterpreterAction;
use revm_interpreter::opcode::make_instruction_table;
use revm_interpreter::primitives::specification::CancunSpec;
use revm_interpreter::primitives::{address, Bytecode, Bytes, U256};
use revm_interpreter::DummyHost;

const OPCODES: [u8; 2] = [0x39, 0x00]; // CODECOPY, STOP

const MEMORY_SIZE: usize = 256;

#[unsafe(no_mangle)]
pub static mut CODE: [u8; 32] = [
    0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f,
    0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1a, 0x1b, 0x1c, 0x1d, 0x1e, 0x1f,
];

#[unsafe(no_mangle)]
pub static mut CODE_SIZE: u8 = 32;

#[unsafe(no_mangle)]
pub static mut DEST_OFFSET: u8 = 0;

#[unsafe(no_mangle)]
pub static mut COPY_OFFSET: u8 = 0;

#[unsafe(no_mangle)]
pub static mut COPY_SIZE: u8 = 32;

#[unsafe(no_mangle)]
pub static mut INDEX: u8 = 3;


fn main() {
    // Given

    unsafe {
        // assume CODE_SIZE <= 32
        if CODE_SIZE > 32 {
            return
        }

        // assume COPY_OFFSET + COPY_SIZE <= CODE_SIZE + 2
        if (COPY_OFFSET as u16 + COPY_SIZE as u16) > CODE_SIZE as u16 + 2 {
            return
        }

        // assume DEST_OFFEST + COPY_SIZE <= MEMORY_SIZE
        if (DEST_OFFSET as usize + COPY_SIZE as usize) > MEMORY_SIZE {
            return
        }

        // assume INDEX < COPY_SIZE
        if INDEX >= COPY_SIZE {
            return
        }
    }

    let input = Bytes::from([]);
    let bytecode_iter = unsafe {
        OPCODES.iter().chain(CODE[..CODE_SIZE as usize].iter())
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

    let Ok(()) = interpreter.stack.push(U256::from(unsafe { COPY_SIZE })) else {
        panic!()
    };
    let Ok(()) = interpreter.stack.push(U256::from(unsafe { COPY_OFFSET })) else {
        panic!()
    };
    let Ok(()) = interpreter.stack.push(U256::from(unsafe { DEST_OFFSET })) else {
        panic!()
    };

    let memory = SharedMemory::with_capacity(MEMORY_SIZE);
    let instruction_table = make_instruction_table::<DummyHost, CancunSpec>();
    let mut host = DummyHost::default();

    // When
    let action = interpreter.run(memory, &instruction_table, &mut host);

    // Then
    let InterpreterAction::Return { result: _ } = action else {
        panic!()
    };
    unsafe {
        let expected = if INDEX < 2 {
            OPCODES[INDEX as usize]
        } else {
            CODE[INDEX as usize - 2]        
        };
        let actual = interpreter.shared_memory.get_byte(DEST_OFFSET as usize + INDEX as usize);
        if actual != expected {
            panic!()
        }
    }
}
