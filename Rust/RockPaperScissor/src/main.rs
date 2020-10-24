use std::io;
use rand::Rng;


fn determine_winner(player: usize, computer: usize) -> () {
     if player == computer {
         println!("Tie !");
     }
     else {
         match player {
             0 => if computer == 1 {println!("Computer wins !\n")} else {println!("You win !\n")},
             1 => if computer == 2 {println!("Computer wins !\n")} else {println!("You win !\n")},
             2 => if computer == 0 {println!("Computer wins !\n")} else {println!("You win !\n")},
             _ => (),
         };
     }
}

fn game_choice() -> usize {
    const PLAYS: [&str; 3] = ["Rock", "Paper", "Scissor"];
    let mut choice = String::new();
    println!("Choose :");
    let ch: usize = loop {
                    for (i, p) in PLAYS.iter().enumerate() {
                        println!("{}){}",i+1,p);
                    }println!("4) Back to menu");   

                    io::stdin()
                        .read_line(&mut choice)
                        .expect("Failed to read line");
                    let ch: usize = match choice.trim().parse() {
                                    Ok(num) => num,
                                    Err(_) => continue,
                                };
                    break ch-1;
                };
    ch
}

fn play(mode: u64) -> () {

    const PLAYS: [&str;3] = ["Rock", "Paper", "Scissor"];
    loop {
        let player_choice: usize = game_choice();
        let random_index: usize = if mode == 1 {
                                    rand::thread_rng().gen_range(0, 3)
                                } else {
                                    match player_choice {
                                        0 => 1,
                                        1 => 2,
                                        2 => 0,
                                        num => num,
                                    }
                                };

        if player_choice == 3 {
            break;
        }

        match player_choice {
            0..=2 => {
                    println!("You choose {}\nComputer chooses {}",PLAYS[player_choice], PLAYS[random_index]); 
                    determine_winner(player_choice, random_index);
            },
               _ => continue,
        };
    }
}

fn main() {
    loop {
        println!("Choose a mode:\n1) Impossible\n2) Random");
        let mut mode: String = String::new();
        io::stdin()
            .read_line(&mut mode)
            .expect("Failed to read line");

        let mode: u64 = match mode.trim().parse() {
            Ok(num) => num,
            Err(_) => continue,
        };

        match mode {
            1 => play(0),
            2 => play(1),
            _ => continue,
        }
    }
}

