Thanks for the opportunity
please found the instruction running the tests:
for specific test type (Negative or Positive)run the command "pytest -vs test_file_name.py"
for running all together simply run "pytest -vs"

Note:
in the GUI assert the navbar and check if the elements are enabled
I did some assert for the submenu checking the correction test element and the number of exists elements

for the question: There are at least two bugs in one of the methods of the service, what are they? What tests
should be applied to find them?
I found that the Delete User API not deleting the user and response with wrong status code and not returning new list
the tests are : running the delete user and verify the user is not exists in DB by GET API
