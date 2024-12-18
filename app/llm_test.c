#include <assert.h>
#include "snake/state.h"

void test_create_default_state(void) {
    game_state_t* state = create_default_state();
    
    // Test that state was created successfully
    assert(state != NULL);
    
    // Test default board dimensions
    assert(state->num_rows > 0);
    assert(state->board != NULL);
    
    // Test snake initialization
    assert(state->num_snakes > 0);
    assert(state->snakes != NULL);
    
    // Test that first snake is alive
    assert(state->snakes[0].live == true);
    
    // Clean up
    free_state(state);
}

int main(void) {
    test_create_default_state();
    printf("All tests passed!\n");
    return 0;
}