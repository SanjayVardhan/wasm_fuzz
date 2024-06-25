(module
  (memory 1)
  (func $nop (export "nop")
    i32.const 1
    i32.const 0xdead
    i32.store
  )

  (func (export "nop2")
    nop
    i32.const 0
    i32.const 0xdead
    i32.store
    i32.const 1
    i32.const 0xdead
    i32.store
  )
)
