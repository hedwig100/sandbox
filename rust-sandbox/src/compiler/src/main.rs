mod lexer;

use std::env;
use std::process::ExitCode;

fn prefix() -> &'static str {
    ".intel_syntax noprefix"
}

fn main() -> ExitCode {
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        println!("Usage: compiler <source file>");
        return ExitCode::from(1);
    }

    println!("{}", prefix());
    println!(".global main");
    println!("main:");
    println!("  mov rax, {}", args[1]);
    println!("  ret");
    ExitCode::from(0)
}
