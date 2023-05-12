#lang forge

option problem_type temporal

one sig Width {
    width: one Int
}

pred setWidth {
    Width.width = 5
}

one sig Height {
    height: one Int
}

pred setHeight {
    Height.height = 5
}

sig Position {
    adjacent: set Position,
    coordinates: pfunc Int->Int,
    row: one Int,
    column: one Int
}

pred validPosition {
    all p: Position | {
        p.column >= 0
        p.column < Width.width
        p.row >= 0
        p.row < Height.height
        p.coordinates = row->column
    }
}

abstract sig Status {}

one sig Lost, Won, Play extends Status {}

sig State {
    walls : set Position,
    food : set Position,
    pacman : one Position,
    ghost : one Position,
    status : one Status
}

pred facts {
    -- TODO: SPLIT ALL THESE INTO SEPARATE PREDS

    // no duplicate positions
    all p1, p2: Position | {
        (p1 != p2) => (p1.column != p2.column) or (p1.row != p2.row)
    }

    // establish adjacent positions
    all p, a: Position | {
        (a in p.adjacent) iff 
            ((a.row = p.row) and (
                (a.column = add[1, p.column]) or
                (a.column = subtract[p.column, 1])
            ))
            or
            ((a.column = p.column) and (
                (a.row = add[1, p.row]) or
                (a.row = subtract[p.row, 1])
            ))
    } 

    // Adjacent columns differ by one, adjacent rows differ by Width
    all p: Position {
        some a: Int, b: Int | {
            a = multiply[p.row, Width.width]
            b = multiply[p'.row, Width.width]
            add[a, p.column] < add[b, p'.column]
        }
    }

    // win game if all food is eaten
    all s: State | {
        s.status = Won iff s.food = none
    }

    // lose game if ghost and pacman at same position
    all s: State | {
        s.status = Lost iff s.ghost = s.pacman
    }
}

pred foodNeverIncreases[s: State] {
    s'.food in s.food
}

pred eatFood[s: State] {
    s'.food = s.food - s.pacman
}

pred wallsDontMove[s: State] {
    s.walls = s'.walls
}

pred adjacentMovement[s: State] {
    (s'.pacman->s.pacman in s'.pacman.adjacent) and (not (s.pacman in s.walls or s'.pacman in s'.walls))
    (s'.ghost->s.ghost in s'.ghost.adjacent) and (not (s.ghost in s.walls or s'.ghost in s'.walls))
}

pred movementOnlyWhenPlaying[s: State] {
    s.status != Play implies s = s'
}

pred ValidBehavior {
    all s: State | {
        foodNeverIncreases[s] and
        eatFood[s] and 
        wallsDontMove[s] and
        adjacentMovement[s] and
        movementOnlyWhenPlaying[s] and
        facts and
        validPosition and
        setWidth and
        setHeight and
        init[]
    }
}

pred init[s: State] {
    s.walls.coordinates = 3->0 + 3->1 + 3->2 and
    s.food.coordinates = 0->0 + 1->0 + Int[2]->Int[0] + Int[0]->Int[1] + Int[1]->Int[1] + Int[2]->Int[1] + Int[0]->Int[2] + Int[1]->Int[2] +Int[2]->Int[2] and
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

run GameLost for 10 State, exactly 25 Position, 6 int