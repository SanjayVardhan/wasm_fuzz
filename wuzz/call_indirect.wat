(module
  (type $add_t (func (param i32 i32) (result i32)))

  (table 2 funcref)
  (elem (i32.const 0) $add)

  (func $add (type $add_t) (param i32 i32) (result i32)
    local.get 0
    local.get 1
    i32.add
  )

  (func $main (result i32)
    i32.const 5
    i32.const 3
    i32.const 0
    call_indirect (type $add_t)
  )

  (export "main" (func $main))
)
