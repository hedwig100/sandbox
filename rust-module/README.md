# Rust-module

Understand rust's module system.

## Objects related to module system in Rust
### Workspace
Workspace is not explanined here.

### Crate
A crate has a Cargo.toml that describes dependencies, package name, e.t.c,.
This is a compile unit of rust.

### Module
A module has a `mod.rs` or `<modulename>.rs`. 

In this repository, The `adder` folder is a module which has several files. 
This module has a `mod.rs`. 

The `mul.rs` is a module which consists of one file.

## How to import module or crate?
### Crate
Crates are imported in `Cargo.toml`. If you use workspace, you have several crates.
In this case, in each `Cargo.toml`, you can declare dependencies of the crate.
The crate can import not only external crates but also internal crates via file path.

### Module
A module is imported by `mod <modulename>`. The `mod <modulename>` is also used when modules are declared in `mod.rs`.

### Abbreviation of module path
If you want to abbreviate a module path like `adder::add::add`, the `use <path>` is used.
The `use` is used only in this style. `use crate::adder::add` is used to abbreviate a path in its own crate.

If you want to use another module 
in the same module (e.g. want to use `sub.rs` from `add.rs`), you can use this 
to rename the module (e.g. `use super::sub` instead of `crate::adder::sub`).

### Execption
`main.rs` is a exceptional module which is called the root module. 
In `main.rs`, `mod <module>` 