<table>
<thead>
<tr>
<th>
Test ID
</th>
<th>
Template
</th>
<th>
Context
</th>
<th>
Symbolic Names
</th>
</tr>
</thead>
<tbody>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/stop-test-sp1.k"><code>stop-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/stop-test"><code>stop-test</code></a>
</td>
<td>
</td>
<td>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/add-test-sp1.k"><code>add-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/simple-2-op-test"><code>simple-2-op-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x01</code>
</td>
</tr>
<tr>
<td>
<code>expected</code>
</td>
<td>
<code>op1.wrapping_add(op0)</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>, <code>OP1</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/mul-test-sp1.k"><code>mul-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/simple-2-op-test"><code>simple-2-op-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x02</code>
</td>
</tr>
<tr>
<td>
<code>expected</code>
</td>
<td>
<code>op1.wrapping_mul(op0)</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>, <code>OP1</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/sub-test-sp1.k"><code>sub-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/simple-2-op-test"><code>simple-2-op-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x03</code>
</td>
</tr>
<tr>
<td>
<code>expected</code>
</td>
<td>
<code>op1.wrapping_sub(op0)</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>, <code>OP1</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/div-test-sp1.k"><code>div-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/simple-2-op-test"><code>simple-2-op-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x04</code>
</td>
</tr>
<tr>
<td>
<code>expected</code>
</td>
<td>
<code>op1.wrapping_div(op0)</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>, <code>OP1</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/sdiv-test-sp1.k"><code>sdiv-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/simple-2-op-test"><code>simple-2-op-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x05</code>
</td>
</tr>
<tr>
<td>
<code>expected</code>
</td>
<td>
<pre>
<code class="language-rust">
use revm_interpreter::instructions::i256::i256_div;
&nbsp;
i256_div(op1, op0)
</code>
</pre>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>, <code>OP1</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/mod-test-sp1.k"><code>mod-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/simple-2-op-test"><code>simple-2-op-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x06</code>
</td>
</tr>
<tr>
<td>
<code>expected</code>
</td>
<td>
<code>op1.wrapping_rem(op1)</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>, <code>OP1</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/smod-test-sp1.k"><code>smod-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/simple-2-op-test"><code>simple-2-op-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x07</code>
</td>
</tr>
<tr>
<td>
<code>expected</code>
</td>
<td>
<pre>
<code class="language-rust">
use revm_interpreter::instructions::i256::i256_mod;
&nbsp;
i256_mod(op1, op0)
</code>
</pre>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>, <code>OP1</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/addmod-test-sp1.k"><code>addmod-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/simple-3-op-test"><code>simple-3-op-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x08</code>
</td>
</tr>
<tr>
<td>
<code>expected</code>
</td>
<td>
<code>op2.add_mod(op1, op0)</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>, <code>OP1</code>, <code>OP2</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/mulmod-test-sp1.k"><code>mulmod-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/simple-3-op-test"><code>simple-3-op-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x09</code>
</td>
</tr>
<tr>
<td>
<code>expected</code>
</td>
<td>
<code>op2.mul_mod(op1, op0)</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>, <code>OP1</code>, <code>OP2</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/exp-test-sp1.k"><code>exp-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/simple-2-op-test"><code>simple-2-op-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x0a</code>
</td>
</tr>
<tr>
<td>
<code>expected</code>
</td>
<td>
<code>op1.pow(op0)</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>, <code>OP1</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/signextend-test-sp1.k"><code>signextend-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/simple-2-op-test"><code>simple-2-op-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x0b</code>
</td>
</tr>
<tr>
<td>
<code>expected</code>
</td>
<td>
<pre>
<code class="language-rust">
if op1 < U256::from(31) {
    let op1 = op1.as_limbs()[0];
    let bit_index = (8 * op1 + 7) as usize;
    let bit = op0.bit(bit_index);
    let mask = (U256::from(1) << bit_index) - U256::from(1);
    if bit {
        op0 | !mask
    } else {
        op0 & mask
    }
} else {
    op0
}
</code>
</pre>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>, <code>OP1</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/lt-test-sp1.k"><code>lt-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/simple-2-op-test"><code>simple-2-op-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x10</code>
</td>
</tr>
<tr>
<td>
<code>expected</code>
</td>
<td>
<code>U256::from(op1 < op0)</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>, <code>OP1</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/gt-test-sp1.k"><code>gt-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/simple-2-op-test"><code>simple-2-op-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x11</code>
</td>
</tr>
<tr>
<td>
<code>expected</code>
</td>
<td>
<code>U256::from(op1 > op0)</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>, <code>OP1</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/slt-test-sp1.k"><code>slt-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/simple-2-op-test"><code>simple-2-op-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x12</code>
</td>
</tr>
<tr>
<td>
<code>expected</code>
</td>
<td>
<pre>
<code class="language-rust">
use core::cmp::Ordering;
use revm_interpreter::instructions::i256::i256_cmp;
&nbsp;
U256::from(i256_cmp(&op1, &op0) == Ordering::Less)
</code>
</pre>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>, <code>OP1</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/sgt-test-sp1.k"><code>sgt-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/simple-2-op-test"><code>simple-2-op-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x13</code>
</td>
</tr>
<tr>
<td>
<code>expected</code>
</td>
<td>
<pre>
<code class="language-rust">
use core::cmp::Ordering;
use revm_interpreter::instructions::i256::i256_cmp;
&nbsp;
U256::from(i256_cmp(&op1, &op0) == Ordering::Greater)
</code>
</pre>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>, <code>OP1</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/eq-test-sp1.k"><code>eq-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/simple-2-op-test"><code>simple-2-op-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x14</code>
</td>
</tr>
<tr>
<td>
<code>expected</code>
</td>
<td>
<code>U256::from(op1 == op0)</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>, <code>OP1</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/iszero-test-sp1.k"><code>iszero-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/simple-1-op-test"><code>simple-1-op-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x15</code>
</td>
</tr>
<tr>
<td>
<code>expected</code>
</td>
<td>
<code>U256::from(op0.is_zero())</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/and-test-sp1.k"><code>and-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/simple-2-op-test"><code>simple-2-op-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x16</code>
</td>
</tr>
<tr>
<td>
<code>expected</code>
</td>
<td>
<code>op1 & op0</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>, <code>OP1</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/or-test-sp1.k"><code>or-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/simple-2-op-test"><code>simple-2-op-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x17</code>
</td>
</tr>
<tr>
<td>
<code>expected</code>
</td>
<td>
<code>op1 | op0</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>, <code>OP1</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/xor-test-sp1.k"><code>xor-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/simple-2-op-test"><code>simple-2-op-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x18</code>
</td>
</tr>
<tr>
<td>
<code>expected</code>
</td>
<td>
<code>op1 ^ op0</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>, <code>OP1</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/not-test-sp1.k"><code>not-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/simple-1-op-test"><code>simple-1-op-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x19</code>
</td>
</tr>
<tr>
<td>
<code>expected</code>
</td>
<td>
<code>!op0</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/byte-test-sp1.k"><code>byte-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/simple-2-op-test"><code>simple-2-op-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x1a</code>
</td>
</tr>
<tr>
<td>
<code>expected</code>
</td>
<td>
<pre>
<code class="language-rust">
if op1 < U256::from(32) {
    U256::from(op0.byte(31 - usize::try_from(op1).unwrap()))
} else {
    U256::ZERO
}
</code>
</pre>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>, <code>OP1</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/shl-test-sp1.k"><code>shl-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/simple-2-op-test"><code>simple-2-op-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x1b</code>
</td>
</tr>
<tr>
<td>
<code>expected</code>
</td>
<td>
<pre>
<code class="language-rust">
if op1 < U256::from(256) {
    op0 << op1
} else {
    U256::ZERO
}
</code>
</pre>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>, <code>OP1</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/shr-test-sp1.k"><code>shr-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/simple-2-op-test"><code>simple-2-op-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x1c</code>
</td>
</tr>
<tr>
<td>
<code>expected</code>
</td>
<td>
<pre>
<code class="language-rust">
if op1 < U256::from(256) {
    op0 >> op1
} else {
    U256::ZERO
}
</code>
</pre>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>, <code>OP1</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/sar-test-sp1.k"><code>sar-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/simple-2-op-test"><code>simple-2-op-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x1d</code>
</td>
</tr>
<tr>
<td>
<code>expected</code>
</td>
<td>
<pre>
<code class="language-rust">
if op1 < U256::from(256) {
    op0.arithmetic_shr(usize::try_from(op1).unwrap())
} else if op0.bit(255) {
    U256::MAX
} else {
    U256::ZERO
}
</code>
</pre>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>, <code>OP1</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/keccak256-test-sp1.k"><code>keccak256-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/keccak256-test"><code>keccak256-test</code></a>
</td>
<td>
</td>
<td>
<code>DATA</code>, <code>OFFSET</code>, <code>SIZE</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/address-test-sp1.k"><code>address-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/address-test"><code>address-test</code></a>
</td>
<td>
</td>
<td>
<code>VALUE</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/origin-test-sp1.k"><code>origin-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/host-property-address-test"><code>host-property-address-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x32</code>
</td>
</tr>
<tr>
<td>
<code>property</code>
</td>
<td>
<code>env.tx.caller</code>
</td>
</tr>
</table>
</td>
<td>
<code>VALUE</code>, <code>INDEX</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/caller-test-sp1.k"><code>caller-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/caller-test"><code>caller-test</code></a>
</td>
<td>
</td>
<td>
<code>VALUE</code>, <code>INDEX</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/callvalue-test-sp1.k"><code>callvalue-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/callvalue-test"><code>callvalue-test</code></a>
</td>
<td>
</td>
<td>
<code>VALUE</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/calldataload-test-sp1.k"><code>calldataload-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/calldataload-test"><code>calldataload-test</code></a>
</td>
<td>
</td>
<td>
<code>DATA</code>, <code>DATA_SIZE</code>, <code>LOAD_INDEX</code>, <code>INDEX</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/calldatasize-test-sp1.k"><code>calldatasize-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/calldatasize-test"><code>calldatasize-test</code></a>
</td>
<td>
</td>
<td>
<code>DATA</code>, <code>DATA_SIZE</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/calldatacopy-test-sp1.k"><code>calldatacopy-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/calldatacopy-test"><code>calldatacopy-test</code></a>
</td>
<td>
</td>
<td>
<code>DATA</code>, <code>DATA_SIZE</code>, <code>DEST_OFFSET</code>, <code>OFFSET</code>, <code>SIZE</code>, <code>INDEX</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/codesize-test-sp1.k"><code>codesize-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/codesize-test"><code>codesize-test</code></a>
</td>
<td>
</td>
<td>
<code>CODE</code>, <code>CODE_SIZE</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/codecopy-test-sp1.k"><code>codecopy-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/codecopy-test"><code>codecopy-test</code></a>
</td>
<td>
</td>
<td>
<code>CODE</code>, <code>CODE_SIZE</code>, <code>DEST_OFFSET</code>, <code>OFFSET</code>, <code>SIZE</code>, <code>INDEX</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/gasprice-test-sp1.k"><code>gasprice-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/host-property-u256-test"><code>host-property-u256-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x3a</code>
</td>
</tr>
<tr>
<td>
<code>property</code>
</td>
<td>
<code>env.tx.gas_price</code>
</td>
</tr>
</table>
</td>
<td>
<code>VALUE</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/returndatasize-test-sp1.k"><code>returndatasize-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/returndatasize-test"><code>returndatasize-test</code></a>
</td>
<td>
</td>
<td>
<code>DATA</code>, <code>DATA_SIZE</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/returndatacopy-test-sp1.k"><code>returndatacopy-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/returndatacopy-test"><code>returndatacopy-test</code></a>
</td>
<td>
</td>
<td>
<code>DATA</code>, <code>DATA_SIZE</code>, <code>DEST_OFFSET</code>, <code>OFFSET</code>, <code>SIZE</code>, <code>INDEX</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/coinbase-test-sp1.k"><code>coinbase-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/host-property-address-test"><code>host-property-address-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x41</code>
</td>
</tr>
<tr>
<td>
<code>property</code>
</td>
<td>
<code>env.block.coinbase</code>
</td>
</tr>
</table>
</td>
<td>
<code>VALUE</code>, <code>INDEX</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/timestamp-test-sp1.k"><code>timestamp-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/host-property-u256-test"><code>host-property-u256-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x42</code>
</td>
</tr>
<tr>
<td>
<code>property</code>
</td>
<td>
<code>env.block.timestamp</code>
</td>
</tr>
</table>
</td>
<td>
<code>VALUE</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/number-test-sp1.k"><code>number-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/host-property-u256-test"><code>host-property-u256-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x43</code>
</td>
</tr>
<tr>
<td>
<code>property</code>
</td>
<td>
<code>env.block.number</code>
</td>
</tr>
</table>
</td>
<td>
<code>VALUE</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/prevrandao-test-sp1.k"><code>prevrandao-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/prevrandao-test"><code>prevrandao-test</code></a>
</td>
<td>
</td>
<td>
<code>VALUE</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/gaslimit-test-sp1.k"><code>gaslimit-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/host-property-u256-test"><code>host-property-u256-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x45</code>
</td>
</tr>
<tr>
<td>
<code>property</code>
</td>
<td>
<code>env.block.gas_limit</code>
</td>
</tr>
</table>
</td>
<td>
<code>VALUE</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/chainid-test-sp1.k"><code>chainid-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/chainid-test"><code>chainid-test</code></a>
</td>
<td>
</td>
<td>
<code>VALUE</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/basefee-test-sp1.k"><code>basefee-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/host-property-u256-test"><code>host-property-u256-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x48</code>
</td>
</tr>
<tr>
<td>
<code>property</code>
</td>
<td>
<code>env.block.basefee</code>
</td>
</tr>
</table>
</td>
<td>
<code>VALUE</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/blobhash-test-sp1.k"><code>blobhash-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/blobhash-test"><code>blobhash-test</code></a>
</td>
<td>
</td>
<td>
<code>INDEX</code>, <code>VALUE</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/blobbasefee-test-sp1.k"><code>blobbasefee-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/blobbasefee-test"><code>blobbasefee-test</code></a>
</td>
<td>
</td>
<td>
<code>VALUE</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/pop-test-sp1.k"><code>pop-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/pop-test"><code>pop-test</code></a>
</td>
<td>
</td>
<td>
<code>VALUE</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/mload-test-sp1.k"><code>mload-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/mload-test"><code>mload-test</code></a>
</td>
<td>
</td>
<td>
<code>DATA</code>, <code>OFFSET</code>, <code>INDEX</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/mload-concrete-offset-test-sp1.k"><code>mload-concrete-offset-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/mload-test"><code>mload-test</code></a>
</td>
<td>
</td>
<td>
<code>DATA</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/mstore-test-sp1.k"><code>mstore-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/mstore-test"><code>mstore-test</code></a>
</td>
<td>
</td>
<td>
<code>OFFSET</code>, <code>VALUE</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/mstore-concrete-offset-test-sp1.k"><code>mstore-concrete-offset-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/mstore-test"><code>mstore-test</code></a>
</td>
<td>
</td>
<td>
<code>VALUE</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/mstore8-test-sp1.k"><code>mstore8-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/mstore8-test"><code>mstore8-test</code></a>
</td>
<td>
</td>
<td>
<code>OFFSET</code>, <code>VALUE</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/sload-test-sp1.k"><code>sload-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/sload-test"><code>sload-test</code></a>
</td>
<td>
</td>
<td>
<code>KEY</code>, <code>VALUE</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/sload-concrete-key-test-sp1.k"><code>sload-concrete-key-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/sload-test"><code>sload-test</code></a>
</td>
<td>
</td>
<td>
<code>VALUE</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/sload-concrete-value-test-sp1.k"><code>sload-concrete-value-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/sload-test"><code>sload-test</code></a>
</td>
<td>
</td>
<td>
<code>KEY</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/sstore-test-sp1.k"><code>sstore-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/sstore-test"><code>sstore-test</code></a>
</td>
<td>
</td>
<td>
<code>KEY</code>, <code>VALUE</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/sstore-concrete-key-test-sp1.k"><code>sstore-concrete-key-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/sstore-test"><code>sstore-test</code></a>
</td>
<td>
</td>
<td>
<code>VALUE</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/sstore-concrete-value-test-sp1.k"><code>sstore-concrete-value-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/sstore-test"><code>sstore-test</code></a>
</td>
<td>
</td>
<td>
<code>KEY</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/jump-test-sp1.k"><code>jump-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/jump-test"><code>jump-test</code></a>
</td>
<td>
</td>
<td>
<code>CODE</code>, <code>CODE_SIZE</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/jumpi-test-sp1.k"><code>jumpi-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/jumpi-test"><code>jumpi-test</code></a>
</td>
<td>
</td>
<td>
<code>CODE</code>, <code>CODE_SIZE</code>, <code>COND</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/pc-test-sp1.k"><code>pc-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/pc-test"><code>pc-test</code></a>
</td>
<td>
</td>
<td>
<code>CODE</code>, <code>PC</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/msize-test-sp1.k"><code>msize-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/msize-test"><code>msize-test</code></a>
</td>
<td>
</td>
<td>
<code>SIZE</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/gas-test-sp1.k"><code>gas-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/gas-test"><code>gas-test</code></a>
</td>
<td>
</td>
<td>
<code>GAS_LIMIT</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/tload-test-sp1.k"><code>tload-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/tload-test"><code>tload-test</code></a>
</td>
<td>
</td>
<td>
<code>KEY</code>, <code>VALUE</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/tload-concrete-key-test-sp1.k"><code>tload-concrete-key-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/tload-test"><code>tload-test</code></a>
</td>
<td>
</td>
<td>
<code>VALUE</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/tload-concrete-value-test-sp1.k"><code>tload-concrete-value-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/tload-test"><code>tload-test</code></a>
</td>
<td>
</td>
<td>
<code>KEY</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/tstore-test-sp1.k"><code>tstore-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/tstore-test"><code>tstore-test</code></a>
</td>
<td>
</td>
<td>
<code>KEY</code>, <code>VALUE</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/tstore-concrete-key-test-sp1.k"><code>tstore-concrete-key-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/tstore-test"><code>tstore-test</code></a>
</td>
<td>
</td>
<td>
<code>VALUE</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/tstore-concrete-value-test-sp1.k"><code>tstore-concrete-value-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/tstore-test"><code>tstore-test</code></a>
</td>
<td>
</td>
<td>
<code>KEY</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/mcopy-test-sp1.k"><code>mcopy-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/mcopy-test"><code>mcopy-test</code></a>
</td>
<td>
</td>
<td>
<code>DATA</code>, <code>DEST_OFFSET</code>, <code>SRC_OFFSET</code>, <code>SIZE</code>, <code>INDEX</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/push0-test-sp1.k"><code>push0-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/push-test"><code>push-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x5f</code>
</td>
</tr>
<tr>
<td>
<code>n</code>
</td>
<td>
<code>0</code>
</td>
</tr>
</table>
</td>
<td>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/push1-test-sp1.k"><code>push1-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/push-test"><code>push-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x60</code>
</td>
</tr>
<tr>
<td>
<code>n</code>
</td>
<td>
<code>1</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/push2-test-sp1.k"><code>push2-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/push-test"><code>push-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x61</code>
</td>
</tr>
<tr>
<td>
<code>n</code>
</td>
<td>
<code>2</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/push3-test-sp1.k"><code>push3-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/push-test"><code>push-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x62</code>
</td>
</tr>
<tr>
<td>
<code>n</code>
</td>
<td>
<code>3</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/push4-test-sp1.k"><code>push4-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/push-test"><code>push-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x63</code>
</td>
</tr>
<tr>
<td>
<code>n</code>
</td>
<td>
<code>4</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/push5-test-sp1.k"><code>push5-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/push-test"><code>push-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x64</code>
</td>
</tr>
<tr>
<td>
<code>n</code>
</td>
<td>
<code>5</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/push6-test-sp1.k"><code>push6-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/push-test"><code>push-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x65</code>
</td>
</tr>
<tr>
<td>
<code>n</code>
</td>
<td>
<code>5</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/push7-test-sp1.k"><code>push7-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/push-test"><code>push-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x66</code>
</td>
</tr>
<tr>
<td>
<code>n</code>
</td>
<td>
<code>7</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/push8-test-sp1.k"><code>push8-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/push-test"><code>push-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x67</code>
</td>
</tr>
<tr>
<td>
<code>n</code>
</td>
<td>
<code>8</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/push9-test-sp1.k"><code>push9-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/push-test"><code>push-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x68</code>
</td>
</tr>
<tr>
<td>
<code>n</code>
</td>
<td>
<code>9</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/push10-test-sp1.k"><code>push10-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/push-test"><code>push-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x69</code>
</td>
</tr>
<tr>
<td>
<code>n</code>
</td>
<td>
<code>10</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/push11-test-sp1.k"><code>push11-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/push-test"><code>push-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x6a</code>
</td>
</tr>
<tr>
<td>
<code>n</code>
</td>
<td>
<code>11</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/push12-test-sp1.k"><code>push12-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/push-test"><code>push-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x6b</code>
</td>
</tr>
<tr>
<td>
<code>n</code>
</td>
<td>
<code>12</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/push13-test-sp1.k"><code>push13-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/push-test"><code>push-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x6c</code>
</td>
</tr>
<tr>
<td>
<code>n</code>
</td>
<td>
<code>13</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/push14-test-sp1.k"><code>push14-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/push-test"><code>push-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x6d</code>
</td>
</tr>
<tr>
<td>
<code>n</code>
</td>
<td>
<code>14</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/push15-test-sp1.k"><code>push15-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/push-test"><code>push-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x6e</code>
</td>
</tr>
<tr>
<td>
<code>n</code>
</td>
<td>
<code>15</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/push16-test-sp1.k"><code>push16-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/push-test"><code>push-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x6f</code>
</td>
</tr>
<tr>
<td>
<code>n</code>
</td>
<td>
<code>16</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/push17-test-sp1.k"><code>push17-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/push-test"><code>push-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x70</code>
</td>
</tr>
<tr>
<td>
<code>n</code>
</td>
<td>
<code>17</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/push18-test-sp1.k"><code>push18-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/push-test"><code>push-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x71</code>
</td>
</tr>
<tr>
<td>
<code>n</code>
</td>
<td>
<code>18</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/push19-test-sp1.k"><code>push19-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/push-test"><code>push-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x72</code>
</td>
</tr>
<tr>
<td>
<code>n</code>
</td>
<td>
<code>19</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/push20-test-sp1.k"><code>push20-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/push-test"><code>push-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x73</code>
</td>
</tr>
<tr>
<td>
<code>n</code>
</td>
<td>
<code>20</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/push21-test-sp1.k"><code>push21-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/push-test"><code>push-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x74</code>
</td>
</tr>
<tr>
<td>
<code>n</code>
</td>
<td>
<code>21</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/push22-test-sp1.k"><code>push22-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/push-test"><code>push-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x75</code>
</td>
</tr>
<tr>
<td>
<code>n</code>
</td>
<td>
<code>22</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/push23-test-sp1.k"><code>push23-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/push-test"><code>push-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x76</code>
</td>
</tr>
<tr>
<td>
<code>n</code>
</td>
<td>
<code>23</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/push24-test-sp1.k"><code>push24-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/push-test"><code>push-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x77</code>
</td>
</tr>
<tr>
<td>
<code>n</code>
</td>
<td>
<code>24</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/push25-test-sp1.k"><code>push25-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/push-test"><code>push-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x78</code>
</td>
</tr>
<tr>
<td>
<code>n</code>
</td>
<td>
<code>25</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/push26-test-sp1.k"><code>push26-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/push-test"><code>push-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x79</code>
</td>
</tr>
<tr>
<td>
<code>n</code>
</td>
<td>
<code>26</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/push27-test-sp1.k"><code>push27-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/push-test"><code>push-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x7a</code>
</td>
</tr>
<tr>
<td>
<code>n</code>
</td>
<td>
<code>27</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/push28-test-sp1.k"><code>push28-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/push-test"><code>push-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x7b</code>
</td>
</tr>
<tr>
<td>
<code>n</code>
</td>
<td>
<code>28</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/push29-test-sp1.k"><code>push29-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/push-test"><code>push-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x7c</code>
</td>
</tr>
<tr>
<td>
<code>n</code>
</td>
<td>
<code>29</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/push30-test-sp1.k"><code>push30-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/push-test"><code>push-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x7d</code>
</td>
</tr>
<tr>
<td>
<code>n</code>
</td>
<td>
<code>30</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/push31-test-sp1.k"><code>push31-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/push-test"><code>push-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x7e</code>
</td>
</tr>
<tr>
<td>
<code>n</code>
</td>
<td>
<code>31</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/push32-test-sp1.k"><code>push32-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/push-test"><code>push-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x7f</code>
</td>
</tr>
<tr>
<td>
<code>n</code>
</td>
<td>
<code>32</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/dup1-test-sp1.k"><code>dup1-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/dup-test"><code>dup-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x80</code>
</td>
</tr>
<tr>
<td>
<code>n</code>
</td>
<td>
<code>1</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/dup2-test-sp1.k"><code>dup2-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/dup-test"><code>dup-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x81</code>
</td>
</tr>
<tr>
<td>
<code>n</code>
</td>
<td>
<code>2</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/dup3-test-sp1.k"><code>dup3-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/dup-test"><code>dup-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x82</code>
</td>
</tr>
<tr>
<td>
<code>n</code>
</td>
<td>
<code>3</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/dup4-test-sp1.k"><code>dup4-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/dup-test"><code>dup-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x83</code>
</td>
</tr>
<tr>
<td>
<code>n</code>
</td>
<td>
<code>4</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/dup5-test-sp1.k"><code>dup5-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/dup-test"><code>dup-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x84</code>
</td>
</tr>
<tr>
<td>
<code>n</code>
</td>
<td>
<code>5</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/dup6-test-sp1.k"><code>dup6-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/dup-test"><code>dup-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x85</code>
</td>
</tr>
<tr>
<td>
<code>n</code>
</td>
<td>
<code>6</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/dup7-test-sp1.k"><code>dup7-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/dup-test"><code>dup-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x86</code>
</td>
</tr>
<tr>
<td>
<code>n</code>
</td>
<td>
<code>7</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/dup8-test-sp1.k"><code>dup8-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/dup-test"><code>dup-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x87</code>
</td>
</tr>
<tr>
<td>
<code>n</code>
</td>
<td>
<code>8</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/dup9-test-sp1.k"><code>dup9-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/dup-test"><code>dup-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x88</code>
</td>
</tr>
<tr>
<td>
<code>n</code>
</td>
<td>
<code>9</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/dup10-test-sp1.k"><code>dup10-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/dup-test"><code>dup-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x89</code>
</td>
</tr>
<tr>
<td>
<code>n</code>
</td>
<td>
<code>10</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/dup11-test-sp1.k"><code>dup11-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/dup-test"><code>dup-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x8a</code>
</td>
</tr>
<tr>
<td>
<code>n</code>
</td>
<td>
<code>11</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/dup12-test-sp1.k"><code>dup12-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/dup-test"><code>dup-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x8b</code>
</td>
</tr>
<tr>
<td>
<code>n</code>
</td>
<td>
<code>12</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/dup13-test-sp1.k"><code>dup13-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/dup-test"><code>dup-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x8c</code>
</td>
</tr>
<tr>
<td>
<code>n</code>
</td>
<td>
<code>13</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/dup14-test-sp1.k"><code>dup14-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/dup-test"><code>dup-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x8d</code>
</td>
</tr>
<tr>
<td>
<code>n</code>
</td>
<td>
<code>14</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/dup15-test-sp1.k"><code>dup15-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/dup-test"><code>dup-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x8e</code>
</td>
</tr>
<tr>
<td>
<code>n</code>
</td>
<td>
<code>15</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/dup16-test-sp1.k"><code>dup16-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/dup-test"><code>dup-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x8f</code>
</td>
</tr>
<tr>
<td>
<code>n</code>
</td>
<td>
<code>16</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/swap1-test-sp1.k"><code>swap1-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/swap-test"><code>swap-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x90</code>
</td>
</tr>
<tr>
<td>
<code>n</code>
</td>
<td>
<code>1</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>, <code>OP1</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/swap2-test-sp1.k"><code>swap2-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/swap-test"><code>swap-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x91</code>
</td>
</tr>
<tr>
<td>
<code>n</code>
</td>
<td>
<code>2</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>, <code>OP1</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/swap3-test-sp1.k"><code>swap3-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/swap-test"><code>swap-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x92</code>
</td>
</tr>
<tr>
<td>
<code>n</code>
</td>
<td>
<code>3</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>, <code>OP1</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/swap4-test-sp1.k"><code>swap4-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/swap-test"><code>swap-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x93</code>
</td>
</tr>
<tr>
<td>
<code>n</code>
</td>
<td>
<code>4</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>, <code>OP1</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/swap5-test-sp1.k"><code>swap5-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/swap-test"><code>swap-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x94</code>
</td>
</tr>
<tr>
<td>
<code>n</code>
</td>
<td>
<code>5</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>, <code>OP1</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/swap6-test-sp1.k"><code>swap6-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/swap-test"><code>swap-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x95</code>
</td>
</tr>
<tr>
<td>
<code>n</code>
</td>
<td>
<code>6</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>, <code>OP1</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/swap7-test-sp1.k"><code>swap7-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/swap-test"><code>swap-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x96</code>
</td>
</tr>
<tr>
<td>
<code>n</code>
</td>
<td>
<code>7</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>, <code>OP1</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/swap8-test-sp1.k"><code>swap8-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/swap-test"><code>swap-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x97</code>
</td>
</tr>
<tr>
<td>
<code>n</code>
</td>
<td>
<code>8</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>, <code>OP1</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/swap9-test-sp1.k"><code>swap9-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/swap-test"><code>swap-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x98</code>
</td>
</tr>
<tr>
<td>
<code>n</code>
</td>
<td>
<code>9</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>, <code>OP1</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/swap10-test-sp1.k"><code>swap10-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/swap-test"><code>swap-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x99</code>
</td>
</tr>
<tr>
<td>
<code>n</code>
</td>
<td>
<code>10</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>, <code>OP1</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/swap11-test-sp1.k"><code>swap11-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/swap-test"><code>swap-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x9a</code>
</td>
</tr>
<tr>
<td>
<code>n</code>
</td>
<td>
<code>11</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>, <code>OP1</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/swap12-test-sp1.k"><code>swap12-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/swap-test"><code>swap-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x9b</code>
</td>
</tr>
<tr>
<td>
<code>n</code>
</td>
<td>
<code>12</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>, <code>OP1</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/swap13-test-sp1.k"><code>swap13-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/swap-test"><code>swap-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x9c</code>
</td>
</tr>
<tr>
<td>
<code>n</code>
</td>
<td>
<code>13</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>, <code>OP1</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/swap14-test-sp1.k"><code>swap14-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/swap-test"><code>swap-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x9d</code>
</td>
</tr>
<tr>
<td>
<code>n</code>
</td>
<td>
<code>14</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>, <code>OP1</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/swap15-test-sp1.k"><code>swap15-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/swap-test"><code>swap-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x9e</code>
</td>
</tr>
<tr>
<td>
<code>n</code>
</td>
<td>
<code>15</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>, <code>OP1</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/swap16-test-sp1.k"><code>swap16-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/swap-test"><code>swap-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0x9f</code>
</td>
</tr>
<tr>
<td>
<code>n</code>
</td>
<td>
<code>16</code>
</td>
</tr>
</table>
</td>
<td>
<code>OP0</code>, <code>OP1</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/log0-test-sp1.k"><code>log0-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/log-test"><code>log-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0xa0</code>
</td>
</tr>
<tr>
<td>
<code>n_topics</code>
</td>
<td>
<code>0</code>
</td>
</tr>
</table>
</td>
<td>
<code>DATA</code>, <code>OFFSET</code>, <code>SIZE</code>, <code>INDEX</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/log1-test-sp1.k"><code>log1-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/log-test"><code>log-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0xa1</code>
</td>
</tr>
<tr>
<td>
<code>n_topics</code>
</td>
<td>
<code>1</code>
</td>
</tr>
</table>
</td>
<td>
<code>DATA</code>, <code>OFFSET</code>, <code>SIZE</code>, <code>INDEX</code>, <code>TOPIC_DATA</code>, <code>TOPIC_INDEX</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/log2-test-sp1.k"><code>log2-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/log-test"><code>log-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0xa2</code>
</td>
</tr>
<tr>
<td>
<code>n_topics</code>
</td>
<td>
<code>2</code>
</td>
</tr>
</table>
</td>
<td>
<code>DATA</code>, <code>OFFSET</code>, <code>SIZE</code>, <code>INDEX</code>, <code>TOPIC_DATA</code>, <code>TOPIC_INDEX</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/log3-test-sp1.k"><code>log3-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/log-test"><code>log-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0xa3</code>
</td>
</tr>
<tr>
<td>
<code>n_topics</code>
</td>
<td>
<code>3</code>
</td>
</tr>
</table>
</td>
<td>
<code>DATA</code>, <code>OFFSET</code>, <code>SIZE</code>, <code>INDEX</code>, <code>TOPIC_DATA</code>, <code>TOPIC_INDEX</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/log4-test-sp1.k"><code>log4-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/log-test"><code>log-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0xa4</code>
</td>
</tr>
<tr>
<td>
<code>n_topics</code>
</td>
<td>
<code>4</code>
</td>
</tr>
</table>
</td>
<td>
<code>DATA</code>, <code>OFFSET</code>, <code>SIZE</code>, <code>INDEX</code>, <code>TOPIC_DATA</code>, <code>TOPIC_INDEX</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/create-test-sp1.k"><code>create-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/create-test"><code>create-test</code></a>
</td>
<td>
</td>
<td>
<code>DATA</code>, <code>VALUE</code>, <code>OFFSET</code>, <code>SIZE</code>, <code>INDEX</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/return-test-sp1.k"><code>return-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/return-with-output-test"><code>return-with-output-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0xf3</code>
</td>
</tr>
<tr>
<td>
<code>instruction_result</code>
</td>
<td>
<code>Return</code>
</td>
</tr>
</table>
</td>
<td>
<code>DATA</code>, <code>OFFSET</code>, <code>SIZE</code>, <code>INDEX</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/create2-test-sp1.k"><code>create2-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/create2-test"><code>create2-test</code></a>
</td>
<td>
</td>
<td>
<code>DATA</code>, <code>VALUE</code>, <code>OFFSET</code>, <code>SIZE</code>, <code>SALT</code>, <code>INDEX</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/revert-test-sp1.k"><code>revert-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/return-with-output-test"><code>return-with-output-test</code></a>
</td>
<td>
<table>
<tr>
<td>
<code>opcode</code>
</td>
<td>
<code>0xfd</code>
</td>
</tr>
<tr>
<td>
<code>instruction_result</code>
</td>
<td>
<code>Revert</code>
</td>
</tr>
</table>
</td>
<td>
<code>DATA</code>, <code>OFFSET</code>, <code>SIZE</code>, <code>INDEX</code>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/specs/invalid-test-sp1.k"><code>invalid-test</code></a>
</td>
<td>
<a href="https://github.com/runtimeverification/zkevm-harness/blob/master/src/tests/integration/test-data/templates/invalid-test"><code>invalid-test</code></a>
</td>
<td>
</td>
<td>
</td>
</tr>
</tbody>
</table>
