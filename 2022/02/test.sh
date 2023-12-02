clear

echo "*** ADVENT CODE 2022 ***"
echo "DAY 2"
echo ""

clang++ -Wall -Wextra -Werror -std=c++20 day_02a.cpp -o puzzle_a
echo "test a: "
./puzzle_a day_02_input
echo ""

clang++ -Wall -Wextra -Werror -std=c++20 day_02b.cpp -o puzzle_b
echo "test b: "
./puzzle_b day_02_input
echo ""

rm puzzle_a puzzle_b