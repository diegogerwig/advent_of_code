clear

clang++ -Wall -Wextra -Werror day_01a.cpp -o day_01a
echo "test day_01a: "
./day_01a day_01_input
echo ""

clang++ -Wall -Wextra -Werror day_01b.cpp -o day_01b
echo "test day_01b: "
./day_01b day_01_input
echo ""

rm day_01a day_01b