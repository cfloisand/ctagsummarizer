// Test File for use by ctag.py

#include <iostream>

int main(int argc, const char **argv)
{
	// TODO: Do something here.
	std::cout << "ctag.py test file.\n";

	// Not a tagged comment.
	std::cout << "Tagged comment after the line."; /* FIXME: Needs a newline. */

	// FIXME: This loop never runs.
	while (0) {
		std::cout << "This will never be seen.\n";
	}


	// TODO: Clear away some space...

	return 0;
}