#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "snake_utils.h"
#include "state.h"

/* Helper function definitions */
static void set_board_at(game_state_t* state, unsigned int x, unsigned int y, char ch);
static bool is_tail(char c);
static bool is_snake(char c);
static char body_to_tail(char c);
static unsigned int get_next_x(unsigned int cur_x, char c);
static unsigned int get_next_y(unsigned int cur_y, char c);
static void find_head(game_state_t* state, unsigned int snum);
static char next_square(game_state_t* state, unsigned int snum);
static void update_tail(game_state_t* state, unsigned int snum);
static void update_head(game_state_t* state, unsigned int snum);


/* Task 1 */
game_state_t* create_default_state() {
  // TODO: Implement this function.

  int i;
  int rows;
  int cols = 20;

  //malloc for snake struct
  snake_t *snake1 = (snake_t *) malloc(sizeof(snake_t));
  snake1->tail_y = 2;
  snake1->tail_x = 2;
  snake1->head_y = 2;
  snake1->head_x = 4;
  snake1->live = true;

  //malloc for state struct
  game_state_t *state = (game_state_t *) malloc(sizeof(game_state_t));
  state->num_rows = 18;
  state->num_snakes = 1;
  state->snakes = snake1;

  //malloc for board rows
  (*state).board = (char**) malloc((*state).num_rows*sizeof(char*));

  rows = (*state).num_rows;

  //malloc for board cols
  for (i = 0; i < rows; i++) {
	  (*state).board[i] = (char*) malloc((cols+1)*sizeof(char));
  }


  //initializing the top row
  for (i = 0; i < cols; i++) {
     (*state).board[0][i] = '#';
  }
 (*state).board[0][cols] = '\0';

  //copy top row to bottom row
  memcpy((*state).board[rows - 1], (*state).board[0], cols+1);

  //initialize row 1
  for (i = 0; i < cols; i++) {
     if (i == 0 || i == cols - 1) {
       (*state).board[1][i] = '#';
     } else {
        (*state).board[1][i] = ' ';
     }
  }
  (*state).board[1][cols] = '\0';

  //copy row 1 to rows 2 through 17
  for (i = 2; i < rows - 1; i++) {
    memcpy((*state).board[i], (*state).board[1], cols+1);
  }

  //initialize food location 
  state->board[2][9] = '*';
  
  //set the snake
  state->board[state->snakes->tail_y][state->snakes->tail_y] = 'd';
  state->board[state->snakes->head_y][state->snakes->head_x] = 'D';
  state->board[2][3] = '>';


  return state;
}


/* Task 2 */
void free_state(game_state_t* state) {
  // TODO: Implement this function.
  
  int i;

  //free all snake pointers
  free(state->snakes);
  //for (i = 0; i < state->num_snakes; i++) {
  //  free(state->snakes + i);
  //}

  //free the board pointers
  for (i = 0; i < state->num_rows; i++) {
    free(state->board[i]);
  }

  free(state->board);

  //free the game_state_t struct
  free(state);
  return;
}

/* Task 3 */
void print_board(game_state_t* state, FILE* fp) {
  // TODO: Implement this function.

  //draw the board
  int i;
  for (i = 0; i < state->num_rows; i++) {
    fprintf(fp, "%s", (*state).board[i]);
    fprintf(fp, "\n");
  }
  return;
}

/*
  Saves the current state into filename. Does not modify the state object.
  (already implemented for you).
*/
void save_board(game_state_t* state, char* filename) {
  FILE* f = fopen(filename, "w");
  print_board(state, f);
  fclose(f);
}


/* Task 4.1 */

/*
  Helper function to get a character from the board
  (already implemented for you).
*/
char get_board_at(game_state_t* state, unsigned int x, unsigned int y) {
  return state->board[y][x];
}

/*
  Helper function to set a character on the board
  (already implemented for you).
*/
static void set_board_at(game_state_t* state, unsigned int x, unsigned int y, char ch) {
  state->board[y][x] = ch;
}

/*
  Returns true if c is part of the snake's tail.
  The snake consists of these characters: "wasd"
  Returns false otherwise.
*/
static bool is_tail(char c) {
  // TODO: Implement this function.
  char *p = strchr("wasd", c);
  if (p == NULL) {
     return false;
  }
  return true;
}
/*
  Returns true if c is part of the snake's head.
  The snake consists of these characters: "WASD"
  Returns false otherwise.
*/
static bool is_head(char c) {
  // TODO: Implement this function.
  char *p = strchr("WASD", c);
  if (p == NULL) {
     return false;
  }
  return true;
}

/*
  Returns true if c is part of the snake.
  The snake consists of these characters: "wasd^<>v"
*/
static bool is_snake(char c) {
  // TODO: Implement this function.
  char *p = strchr("wasd^<>v", c);
  if (p == NULL) {
     return false;
  }
  return true;
}

/*
  Converts a character in the snake's body ("^<>v")
  to the matching character representing the snake's
  tail ("wasd").
*/
static char body_to_tail(char c) {
  // TODO: Implement this function.
  if (is_snake(c) && !is_tail(c)) {
    if (c == '^') {
       c = 'w';
    }
    if (c == '<') {
       c = 'a';
    }
    if (c == 'v') {
       c = 's';
    }
    if (c == '>') {
       c = 'd';
    }
    return c;
  }
  return '?';
}

/*
  Converts a character in the snake's head ("WASD")
  to the matching character representing the snake's
  body ("^<>v").
*/
static char head_to_body(char c) {
  // TODO: Implement this function.
  if (is_head(c)) {
    if (c == 'W') {
       c = '^';
    }
    if (c == 'A') {
       c = '<';
    }
    if (c == 'S') {
       c = 'v';
    }
    if (c == 'D') {
       c = '>';
    }
    return c;
  }
  return '?';
}

/*
  Returns cur_x + 1 if c is '>' or 'd' or 'D'.
  Returns cur_x - 1 if c is '<' or 'a' or 'A'.
  Returns cur_x otherwise.
*/
static unsigned int get_next_x(unsigned int cur_x, char c) {
  // TODO: Implement this function.
  char *p;
  p = strchr(">dD", c);

  if (p != NULL) {
    return cur_x + 1;
  }

  p = strchr("<aA", c);

  if (p != NULL) {
    return cur_x - 1;
  }

  return cur_x;
}

/*
  Returns cur_y - 1 if c is '^' or 'w' or 'W'.
  Returns cur_y + 1 if c is 'v' or 's' or 'S'.
  Returns cur_y otherwise.
*/
static unsigned int get_next_y(unsigned int cur_y, char c) {
  // TODO: Implement this function.
  char *p;
  p = strchr("^wW", c);

  if (p != NULL) {
    return cur_y - 1;
  }

  p = strchr("vsS", c);

  if (p != NULL) {
    return cur_y + 1;
  }

  return cur_y;
}

/*
  Task 4.2

  Helper function for update_state. Return the character in the cell the snake is moving into.

  This function should not modify anything.
*/
static char next_square(game_state_t* state, unsigned int snum) {
  // TODO: Implement this function.
  unsigned int xpos = state->snakes[snum].head_x;
  unsigned int ypos = state->snakes[snum].head_y;
  char c = get_board_at(state, xpos, ypos);
  unsigned int nextxpos = get_next_x(xpos, c);
  unsigned int nextypos = get_next_y(ypos, c);


  return state->board[nextypos][nextxpos];
}


/*
  Task 4.3

  Helper function for update_state. Update the head...

  ...on the board: add a character where the snake is moving

  ...in the snake struct: update the x and y coordinates of the head

  Note that this function ignores food, walls, and snake bodies when moving the head.
*/
static void update_head(game_state_t* state, unsigned int snum) {
  // TODO: Implement this function.
  unsigned int xpos = state->snakes[snum].head_x;
  unsigned int ypos = state->snakes[snum].head_y;
  char c = get_board_at(state, xpos, ypos);

  unsigned int nextxpos = get_next_x(xpos, c);
  unsigned int nextypos = get_next_y(ypos, c);


  state->board[ypos][xpos] = head_to_body(c);
  state->board[nextypos][nextxpos] = c;
  state->snakes[snum].head_x = nextxpos;
  state->snakes[snum].head_y = nextypos;

  return;
}


/*
  Task 4.4

  Helper function for update_state. Update the tail...

  ...on the board: blank out the current tail, and change the new
  tail from a body character (^v<>) into a tail character (wasd)

  ...in the snake struct: update the x and y coordinates of the tail
*/
static void update_tail(game_state_t* state, unsigned int snum) {
  // TODO: Implement this function.
  unsigned int xpos = state->snakes[snum].tail_x;
  unsigned int ypos = state->snakes[snum].tail_y;
  char c = get_board_at(state, xpos, ypos);
  char taildirection;

  unsigned int nextxpos = get_next_x(xpos, c);
  unsigned int nextypos = get_next_y(ypos, c);



  taildirection = state->board[nextypos][nextxpos];
  state->board[ypos][xpos] = ' ';
  state->board[nextypos][nextxpos] = body_to_tail(taildirection);
  state->snakes[snum].tail_x = nextxpos;
  state->snakes[snum].tail_y = nextypos;

  return;
}


/* Task 4.5 */
void update_state(game_state_t* state, int (*add_food)(game_state_t* state)) {
  int i;
  unsigned int xpos;
  unsigned int ypos;
  unsigned int nextxpos;
  unsigned int nextypos;
  char c;
  snake_t* snakes;
  char **board;

  board = state->board;
  snakes = state->snakes;

  for (i = 0; i < state->num_snakes; i++) {
    xpos = snakes[i].head_x;
    ypos = snakes[i].head_y;
    c = board[ypos][xpos];
    nextxpos = get_next_x(xpos, c);
    nextypos = get_next_y(ypos, c);
    if (board[nextypos][nextxpos] == '#' || is_snake(board[nextypos][nextxpos])) {
       //snake dies
       snakes[i].live = false;
       board[ypos][xpos] = 'x';
    } else if (board[nextypos][nextxpos] == '*') {
       //food
       update_head(state, i);
       add_food(state);
    } else {
       //update head, update tail
       update_head(state, i);
       update_tail(state, i);
    }
  }
  return;
}


/* Task 5 */
game_state_t* load_board(char* filename) {
  // TODO: Implement this function.

  //malloc for state struct
  game_state_t *state = (game_state_t *) malloc(sizeof(game_state_t));

  //file
  FILE *file = fopen(filename, "r");

  if (file == NULL) {
    return NULL;
  }

  char c;
  int row;
  row = 0;
  c = fgetc(file);
  for (c; c != EOF; c = getc(file)) {
     if (c == '\n') {
        row += 1;
     }
  }
  rewind(file);

 // state->board = (char**) malloc(size*sizeof(char*));
  char** board = (char**) malloc(row * sizeof(char*));

  char* line;
  char* temp;
  int size = 5;
  line = (char*) malloc(size);
  int i;
  i = 0;
  int j;
  row = 0;

  c = getc(file);
  for (c; c != EOF; c = getc(file)) {
     line[i] = c;
     if (c == '\n') {
       //FIXME could error here, maybe malloc +1 instead
       board[row] = (char*) malloc(2 + i);
       for (j = 0; j <= i; j++) {
          board[row][j] = line[j];
       }
       board[row][i] = '\0';
       row += 1;
       i = 0;
     } else {
       i += 1;
       if (i > size - 2) {
          size += 1;
          line = realloc(line, size);
       }
     }
  }
  fclose(file);
  free(line);
  state->board = board;
  state->num_rows = row;
  return state;
}


/*
  Task 6.1

  Helper function for initialize_snakes.
  Given a snake struct with the tail coordinates filled in,
  trace through the board to find the head coordinates, and
  fill in the head coordinates in the struct.
*/
static void find_head(game_state_t* state, unsigned int snum) {
  snake_t* snakes;
  char **board;
  char* direction;
  unsigned int xpos;
  unsigned int ypos;
  char *next;

  snakes = state->snakes;
  board = state->board;
  ypos = snakes[snum].tail_y;
  xpos = snakes[snum].tail_x;

  next = strchr("s", 's');
  while (next != NULL) {
    direction = board[ypos][xpos];
    next = strchr("sv", direction);
    if (next == NULL) {
      next = strchr("a<", direction);
      if (next == NULL) {
        next = strchr("w^", direction);
        if (next == NULL) {
          next = strchr("d>", direction);
          if (next == NULL) {
            break;
          }
          xpos += 1;
        } else {
           ypos -= 1;
        }
      } else {
        xpos -= 1;
      }
    } else {
       ypos += 1;
    }
  }
  snakes[snum].head_x = xpos;
  snakes[snum].head_y = ypos;
  return;
}


/* Task 6.2 */
game_state_t* initialize_snakes(game_state_t* state) {
  // TODO: Implement this function.
  unsigned int i;
  unsigned int j;
  unsigned int count;
  count = 0;

  for (i = 0; i < state->num_rows; i++) {
     for (j = 0; j < strlen(state->board[i]); j++) {
       if (is_tail(state->board[i][j])) {
         count += 1;
       }
     }
  }

  state->num_snakes = count;
  snake_t *snakes = (snake_t *) malloc(count * sizeof(snake_t));
  state->snakes = snakes;

  count = 0;
  size_t len;
  for (i = 0; i < state->num_rows; i++) {
     len = strlen(state->board[i]);
     for (j = 0; j < len; j++) {
       if (is_tail(state->board[i][j])) {
         state->snakes[count].tail_x = j;
         state->snakes[count].tail_y = i;
         state->snakes[count].live = true;
         find_head(state, count);
         count += 1;
       }
     }
  }
  return state;
}
