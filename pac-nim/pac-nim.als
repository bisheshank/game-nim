open util/ordering[State]
open util/ordering[Position]
open util/integer

one sig Width{
    i: Int
}{
    int[i] = 5
}

one sig Height{
    i: Int
}{
    int[i] = 5
}

sig Position {
    adjacent : set Position,
    coordinates : Int->Int,
    row : Int,
    column : Int
}{
    int[column]>=0
    int[column]<int[Width.i]
    int[row]>=0
    int[row]<int[Height.i]
    coordinates = column->row
}

abstract sig Status {}

one sig Play, Won, Lost extends Status {}

sig State {
    walls : set Position,
    food : set Position,
    pacman : Position,
    blinky : Position,
    status : Status
}


fact NoDuplicatePositions{
    all p1, p2: Position |
    (p1 != p2) => (p1.column!=p2.column) || (p1.row!=p2.row)
}
       

fact AdjacentPositions {
    all p, a: Position{
        (a in p.adjacent) iff{
            int[a.row] = int[p.row] and{
                int[a.column] = int[p.column].add[1] or
                int[a.column] = int[p.column].sub[1]
            }

            or

            int[a.column] = int[p.column] and{
                int[a.row] = int[p.row].add[1] or
                int[a.row] = int[p.row].sub[1]
            }
        }
    }       
}

//Adjacent columns differ by one, adjacent rows differ by Width
fact PositionOrder{
    all p: Position, q: p.next{
        let a = int[p.row].mul[int[Width.i]], b = int[q.row].mul[int[Width.i]]{
            (a + int[p.column]) < (b + int[q.column])
        }
    }
}

fact GameIsWonWhenAllTheFoodIsGone {
    all s : State |
        s.status= Won iff s.food = none
}

fact GameIsLostWhenBlinkyGetsPacman {
    all s : State |
        s.status = Lost iff s.blinky = s.pacman
}

/** PREDICATES - these describe the dynamic state transitions of the model 
/** from the current state (s) to the next state (s') **/
pred FoodSupplyNeverIncreases[s, t : State]
{
    t.food in s.food
}

pred FoodIsEatenByPacman[s, t: State]
{
    t.food = s.food - s.pacman
}

pred WallsDontMove[s, t : State]
{
    s.walls = t.walls
}

pred MovementIsOnlyToAdjacentPosition[s, t:State]
{
    let p = (t.pacman), q = (s.pacman) | (p->q in adjacent) and not(q in s.walls || p in t.walls)
    let p = (t.blinky), q = (s.blinky) |  (p->q in adjacent) and not(q in s.walls || p in t.walls)
}

pred MovementIsPossibleOnlyWhilePlaying[s,t:State]
{
    s.status != Play implies s = t
}

fact ValidBehaviour {
    all s: State, t: s.next {
        FoodSupplyNeverIncreases[s,t] and
        FoodIsEatenByPacman[s,t] and
        MovementIsOnlyToAdjacentPosition[s,t] and
        WallsDontMove[s,t] and
        MovementIsPossibleOnlyWhilePlaying[s,t]
    }
}

pred InitGame[s : State]
{
    s.walls.coordinates = Int[3]->Int[0] + Int[3]->Int[1] + Int[3]->Int[2] and
    s.food.coordinates = Int[0]->Int[0] + Int[1]->Int[0]+ Int[2]->Int[0] + Int[0]->Int[1] + Int[1]->Int[1] + Int[2]->Int[1] + Int[0]->Int[2] + Int[1]->Int[2] +Int[2]->Int[2] and
    s.status = Play
}

pred GameWon {
    last.status = Won
}

pred GameLost {
    last.status = Lost
}

pred GamePlay() {
    last.status = Play
}

fact initialState {
  InitGame[first]
}

/** TRACES - these show that a pacman game run ending in each specified state exists.
    Uncomment as needed.**/
run GameLost {

} for 10 State, exactly 25 Position, 6 int
//run GamePlay for 10 State, exactly 25 Position, 6 int
//run GameLost for 10 State, exactly 25 Position, 6 int
//run GameWon for 10 State, exactly 25 Position, 6 int
