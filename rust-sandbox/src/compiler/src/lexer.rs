use std::io;

pub enum Token {
    Number(i32),

    Reserved(&'static str),

    Eof,
}

pub struct Lexer {
    input: Vec<char>,
    position: usize,
}

impl Lexer {
    pub fn new(input: &str) -> Lexer {
        Lexer {
            input: input.chars().collect(),
            position: 0,
        }
    }

    pub fn tokenize(&mut self) -> io::Result<Vec<Token>> {
        let mut tokens = Vec::new();

        for current_char in self.input.iter() {
            match current_char {
                ' ' => continue,
                ('+', '-') => tokens.push(Token::Reserved(current_char)),

                _ => {
                    if current_char.is_ascii_digit() {
                        let number = self.expect_number()?;
                        tokens.push(Token::Number(number));
                    } else {
                        return Err(io::Error::new(
                            io::ErrorKind::InvalidInput,
                            format!("unexpected character: {}", current_char),
                        ));
                    }
                }
            }
        }

        Ok(tokens)
    }

    fn consume(&mut self, expected: char) -> bool {
        if self.input[self.position] != expected {
            return false;
        }
        self.position += 1;
        true
    }

    fn expect(&mut self, expected: char) -> io::Result<()> {
        if self.input[self.position] != expected {
            return Err(io::Error::new(
                io::ErrorKind::InvalidInput,
                format!(
                    "expect {}, but found {}",
                    expected, self.input[self.position]
                ),
            ));
        }
        self.position += 1;
        Ok(())
    }

    fn expect_number(&mut self) -> io::Result<i32> {
        let mut number = 0;
        let mut is_number = false;
        while self.position < self.input.len() && self.input[self.position].is_ascii_digit() {
            number = number * 10 + self.input[self.position].to_digit(10).unwrap() as i32;
            is_number = true;
            self.position += 1;
        }

        if is_number {
            Ok(number)
        } else {
            Err(io::Error::new(
                io::ErrorKind::InvalidInput,
                format!("expect number, but found {}", self.input[self.position]),
            ))
        }
    }
}
