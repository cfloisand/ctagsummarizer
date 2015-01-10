// Test File for use by ctag.py

#include <iostream>

int main(int argc, const char **argv)
{
	// TODO: Do something here.
	std::cout << "ctag.py test file.\n";

	// Not a tagged comment.
	std::cout << "Tagged comment after the line."; /* FIXME: Needs a newline. */

	// FIXME: This loop never runs. //
	while (0) {
		std::cout << "This will never be seen.\n";
	}

	//TODO: Add space between slashes and tag.

	// TODO: Clear away some space...

	// Here is a block of code that is not tagged, preceding the tagged comment.
	// The code below accumulates by 1 until it reaches 10000.
	// TODO: This block of code is useless.
	int acc = 0;
	while (acc < 10000) {
		acc++;
	}

	/*
	TODO: Keep testing! (I'm in a block).
	 */

	return 0;
}
