# Prompt

What if we were to change the line to "if len(user_transactions) >= max_length:"?

# Response

If you change the condition to `if len(user_transactions) >= max_length:`, the logic will work as follows:

Before adding a new transaction:

1. Check the current length of `user_transactions`.
2. If the current length is equal to or greater than `max_length`, pop the first (oldest) transaction.
3. Append the new transaction to the list.

So, when `len(user_transactions)` is exactly `max_length`, the function will remove the oldest transaction to make space for the new one, ensuring the list length remains at `max_length`.

This change will indeed make the code work correctly for the intended purpose!